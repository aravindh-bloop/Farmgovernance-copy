"""
LLM Reasoner with multi-backend support: Gemini, Groq, and Edge Rule-Grounded Synthesis.
Guarantees graceful degradation — when no external provider is reachable, the system
still produces grounded answers from the verified database (never fabricates facts).

The reasoner is language-aware: it instructs the model to respond *in the user's
language* so the final answer does not depend solely on a fragile translation step.
"""
import os
import re
import json
import hashlib
import threading
import time
from collections import OrderedDict
from typing import Dict, Any, List, Optional

from config.settings import settings


class LLMReasoner:
    # Gemini free tier is ~20 requests/minute per model, so identical questions
    # are served from this short-lived cache instead of burning quota.
    _CACHE_TTL_SECONDS = 900
    _CACHE_MAX_ENTRIES = 200

    def __init__(self):
        self.provider = settings.DEFAULT_LLM_PROVIDER
        self.groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        # Qwen 3.8-27B: fastest on Groq and the strongest of the free models on
        # Indian languages (Tamil/Telugu/Marathi), which the kiosk depends on.
        self.groq_model = getattr(settings, "GROQ_MODEL", None) or os.getenv("GROQ_MODEL") or "qwen/qwen3.8-27b"
        self.gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        self._cache: "OrderedDict[str, tuple]" = OrderedDict()
        self._cache_lock = threading.Lock()

        self._greeting_patterns = [
            r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bnamaste\b", r"\bnamaskar\b",
            r"\bvanakkam\b", r"नमस्ते", r"नमस्कार", r"வணக்கம்", r"నమస్తే",
            r"\bgood morning\b", r"\bgood evening\b", r"\bgood afternoon\b",
            r"\bthanks?\b", r"thank you", r"धन्यवाद", r"நன்றி", r"ధన్యవాదాలు",
            r"\bwho are you\b", r"what are you", r"\bwhat can you do\b",
            r"\bhelp\b", r"मदद", r"உதவி", r"సహాయం", r"\bstart\b",
        ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_response(self, prompt: str, context_docs: List[Dict[str, Any]], domain: str, language: str = "en") -> str:
        if self._llm_enabled():
            if self.gemini_key:
                answer = self._try_gemini(prompt, language)
                if answer:
                    return answer
            if self.groq_key:
                answer = self._try_groq(prompt, language)
                if answer:
                    return answer

        # Edge synthesizer — grounded in the verified database, never hallucinates.
        return self._local_edge_reasoning(context_docs, domain, language)

    def chat(self, messages: List[Dict[str, Any]], system_prompt: str, language: str = "en",
             docs: List[Dict[str, Any]] = None) -> str:
        """
        Multi-turn conversational generation. ``messages`` is a list of
        ``{"role": "user" | "assistant", "content": "..."}`` turns. Used for the
        LLM-first chatbot: the LLM both understands the query and writes the
        answer, grounded on the light-RAG ``docs`` when provided.

        Provider order: Gemini -> Groq -> offline edge synthesis, so a transient
        429/503 from one provider never degrades the conversation.
        """
        if self._llm_enabled():
            if self.gemini_key:
                answer = self._try_gemini_chat(messages, system_prompt, language)
                if answer:
                    return answer
            if self.groq_key:
                answer = self._try_groq_chat(messages, system_prompt, language)
                if answer:
                    return answer
        last_turn = ""
        for turn in reversed(self._normalize_turns(messages)):
            if turn["role"] == "user":
                last_turn = turn["content"]
                break
        return self._local_edge_reasoning(docs or [], "general", language, query=last_turn)

    def _llm_enabled(self) -> bool:
        """Offline/local provider settings must never trigger an external call."""
        return str(self.provider or "").lower() not in ("local_rule_rag", "offline", "none", "edge")

    def is_greeting(self, query: str) -> bool:
        q = (query or "").strip().lower()
        if not q:
            return True  # empty query is treated as a warm-up to avoid hallucinated defaults
        return any(re.search(p, q) for p in self._greeting_patterns)

    def greeting_answer(self) -> str:
        return (
            "Hello! I am the Multilingual Cooperative Assistant. I can guide you on "
            "Cooperative Laws, Government Schemes, PMFBY crop insurance, KCC credit, "
            "PACS services and grievance redressal. Ask me anything — for example: "
            "'How do I apply for PM-KISAN?' or 'My crops were damaged by rain, what do I do?'"
        )

    # ------------------------------------------------------------------
    # Providers
    # ------------------------------------------------------------------
    def _apply_language_instruction(self, prompt: str, language: str) -> str:
        if not language or language == "en":
            return prompt
        return (
            prompt
            + "\n\nIMPORTANT OUTPUT RULE: Write the ENTIRE response in the language whose "
            f"ISO 639-1 code is '{language}'. Use that language's native script. Reply 100% in "
            "{language}, never in English. Keep official names and URLs in English where appropriate."
        )

    @staticmethod
    def _parse_gemini(payload: Dict[str, Any]) -> str:
        candidates = payload.get("candidates", []) or []
        if not candidates:
            return ""
        parts = (candidates[0].get("content", {}) or {}).get("parts", []) or []
        return "".join(part.get("text", "") for part in parts).strip()

    _GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
    _RETRY_STATUSES = (500, 502, 503, 504)

    def _cache_get(self, key: str) -> str:
        with self._cache_lock:
            entry = self._cache.get(key)
            if not entry:
                return ""
            value, stored_at = entry
            if time.time() - stored_at > self._CACHE_TTL_SECONDS:
                self._cache.pop(key, None)
                return ""
            self._cache.move_to_end(key)
            return value

    def _cache_put(self, key: str, value: str) -> None:
        if not value:
            return
        with self._cache_lock:
            self._cache[key] = (value, time.time())
            self._cache.move_to_end(key)
            while len(self._cache) > self._CACHE_MAX_ENTRIES:
                self._cache.popitem(last=False)

    @staticmethod
    def _cache_key(payload: Dict[str, Any]) -> str:
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _inline_system_prompt(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Move systemInstruction text into the first user turn (400 fallback)."""
        system_text = ""
        parts = payload.get("systemInstruction", {}).get("parts", [])
        if parts:
            system_text = parts[0].get("text", "")

        new_payload = {k: v for k, v in payload.items() if k != "systemInstruction"}
        contents = new_payload.get("contents", [])
        if system_text and contents:
            first = contents[0]
            first_text = "".join(p.get("text", "") for p in first.get("parts", []))
            merged = f"{system_text}\n\n---\n{first_text}"
            contents[0] = {"role": first.get("role", "user"), "parts": [{"text": merged}]}
        return new_payload

    def _post_gemini(self, payload: Dict[str, Any], attempts: int = 3) -> str:
        """POST to Gemini with backoff on transient 5xx, and a short cache."""
        import httpx

        cache_key = self._cache_key(payload)
        cached = self._cache_get(cache_key)
        if cached:
            return cached

        last_error = ""
        backoff = (2.0, 5.0)
        inlined = False
        for attempt in range(attempts):
            try:
                response = httpx.post(
                    self._GEMINI_URL,
                    params={"key": self.gemini_key},
                    json=payload,
                    timeout=45.0,
                )
                if response.status_code == 429:
                    # Per-minute quota exhausted: fail over to the next provider
                    # immediately instead of making the farmer wait.
                    print("Gemini quota exhausted (429) — trying the next provider.")
                    break
                if response.status_code in self._RETRY_STATUSES:
                    last_error = f"HTTP {response.status_code}"
                    time.sleep(backoff[min(attempt, len(backoff) - 1)])
                    continue
                if response.status_code == 400 and "systemInstruction" in payload and not inlined:
                    # Some deployments reject the systemInstruction field: inline it
                    # into the first user turn instead of losing the whole answer.
                    inlined = True
                    payload = self._inline_system_prompt(payload)
                    continue
                response.raise_for_status()
                answer = self._parse_gemini(response.json())
                self._cache_put(cache_key, answer)
                return answer
            except Exception as exc:
                last_error = str(exc)
                time.sleep(backoff[min(attempt, len(backoff) - 1)])
        if last_error:
            print(f"Gemini API call failed (falling back): {last_error}")
        return ""

    def _try_gemini(self, prompt: str, language: str) -> str:
        return self._post_gemini({
            "contents": [{"parts": [{"text": self._apply_language_instruction(prompt, language)}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048},
        })

    _GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

    def _post_groq(self, messages: List[Dict[str, str]], temperature: float = 0.3, attempts: int = 3) -> str:
        """Groq chat completion with caching. Primary failover when Gemini is throttled."""
        import time

        import httpx

        cache_key = "groq:" + self._cache_key({"model": self.groq_model, "messages": messages})
        cached = self._cache_get(cache_key)
        if cached:
            return cached

        for attempt in range(attempts):
            try:
                resp = httpx.post(
                    self._GROQ_URL,
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "User-Agent": "cooperative-assistant/1.0",
                    },
                    json={
                        "model": self.groq_model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": 1200,
                    },
                    timeout=45.0,
                )
                if resp.status_code == 200:
                    message = resp.json()["choices"][0]["message"]
                    # gpt-oss models put the answer in `reasoning` when `content` is empty.
                    answer = (message.get("content") or "").strip() or (message.get("reasoning") or "").strip()
                    self._cache_put(cache_key, answer)
                    return answer
                if resp.status_code in (429, 500, 502, 503, 504):
                    # Groq free tier throttles bursts; a couple of seconds is enough.
                    time.sleep(1.5 * (attempt + 1))
                    continue
                print(f"Groq returned HTTP {resp.status_code}")
                return ""
            except Exception as exc:
                print(f"Groq API call failed (falling back): {exc}")
                return ""
        print("Groq rate limit reached after retries (falling back).")
        return ""

    def _try_groq(self, prompt: str, language: str) -> str:
        return self._post_groq(
            [{"role": "user", "content": self._apply_language_instruction(prompt, language)}],
            temperature=0.2,
        )

    @staticmethod
    def _normalize_turns(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Coerce frontend history into Gemini-agnostic user/model turns."""
        turns = []
        for m in messages or []:
            if not isinstance(m, dict):
                continue
            role = str(m.get("role") or m.get("sender") or "").lower()
            content = str(m.get("content") or m.get("text") or "").strip()
            if not content:
                continue
            user = role in ("user", "human", "customer")
            assistant = role in ("assistant", "ai", "bot", "model", "coach", "assistant_model")
            if user or role == "user":
                role = "user"
            elif assistant:
                role = "assistant"
            else:
                continue
            turns.append({"role": role, "content": content})
        return turns[-8:]  # conversational window guard

    def _try_gemini_chat(self, messages: List[Dict[str, Any]], system_prompt: str, language: str) -> str:
        contents = []
        for turn in self._normalize_turns(messages):
            contents.append({
                "role": "model" if turn["role"] == "assistant" else "user",
                "parts": [{"text": turn["content"]}],
            })
        return self._post_gemini({
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048},
        })

    def _try_groq_chat(self, messages: List[Dict[str, Any]], system_prompt: str, language: str) -> str:
        payload = [{"role": "system", "content": system_prompt}]
        for turn in self._normalize_turns(messages):
            payload.append({"role": turn["role"], "content": turn["content"]})
        return self._post_groq(payload)

    @staticmethod
    def _as_list(value: Any) -> List[str]:
        """Coerce a provisions/benefits field into a list of readable strings.

        Some records store these as one long string, which would otherwise be
        sliced character-by-character instead of item-by-item.
        """
        if not value:
            return []
        if isinstance(value, str):
            parts = [p.strip(" -•\t") for p in re.split(r"[;\n]|(?<=[.!?])\s+", value)]
            return [p for p in parts if p] or [value]
        if isinstance(value, dict):
            return [f"{k}: {v}" for k, v in value.items() if v]
        if isinstance(value, (list, tuple)):
            return [str(v) for v in value if v]
        return [str(value)]

    @staticmethod
    def _pick_best_doc(docs: List[Dict[str, Any]], query: str) -> Any:
        """Pick the record whose title matches the words asked about.

        Returns ``(doc, score)`` so callers can tell a real match from a weak one.
        """
        query = query or ""
        q_tokens = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
        # Acronyms / hyphenated scheme names (PM-KISAN, KCC, PMFBY) must match as
        # a phrase, otherwise "Kisan Maan-Dhan" beats "Kisan Samman Nidhi".
        key_terms = [t for t in re.findall(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+|\b[A-Z]{2,}\b", query)]
        key_terms = [t.lower().replace("-", "").replace(" ", "") for t in key_terms]
        if not q_tokens and not key_terms:
            return docs[0], 0
        best, best_score = docs[0], -1
        for doc in docs:
            title = str(doc.get("title") or doc.get("scheme_name") or doc.get("act_name") or "").lower()
            body = str(doc.get("summary") or doc.get("overview") or doc.get("description") or "").lower()
            title_flat = title.replace("-", "").replace(" ", "")
            score = 0
            for term in key_terms:
                if len(term) > 1 and term in title_flat:
                    score += 8
            for token in q_tokens:
                if token in title:
                    score += 3
                elif token in body:
                    score += 1
            if score > best_score:
                best, best_score = doc, score
        return best, best_score

    def _local_edge_reasoning(self, docs: List[Dict[str, Any]], domain: str, language: str,
                              query: str = "") -> str:
        """
        Offline fallback used only when every LLM provider is unreachable.
        Reads the best-matching verified record out loud in plain words so the
        kiosk still gives the farmer something useful instead of a dead end.
        """
        if not docs:
            return (
                "I could not find a verified record matching your question in the official database. "
                "Please contact your local Assistant Registrar of Cooperative Societies (ARCS) or "
                "PACS Secretary with your full details, or rephrase and ask again."
            )

        if query:
            primary_doc, match_score = self._pick_best_doc(docs, query)
        else:
            primary_doc, match_score = docs[0], 0
        title = (
            primary_doc.get("title")
            or primary_doc.get("scheme_name")
            or primary_doc.get("act_name")
            or primary_doc.get("category", "Cooperative Advisory")
        )
        summary = (
            primary_doc.get("summary")
            or primary_doc.get("overview")
            or primary_doc.get("financial_benefit")
            or primary_doc.get("description", "")
        )
        provisions = self._as_list(
            primary_doc.get("key_provisions")
            or primary_doc.get("eligibility_criteria")
            or primary_doc.get("permitted_activities")
            or primary_doc.get("risk_coverage")
        )

        response_lines = []
        if match_score >= 8:
            response_lines += [f"**{title}**", ""]
        else:
            # Weak lexical match: say so instead of presenting a near-random record.
            response_lines += [
                "This is the closest information I have in my records right now (my assistant service is "
                f"busy, so I could not search more widely).",
                "",
                f"**{title}**",
                "",
            ]
        response_lines.append(f"{summary}")

        if provisions:
            response_lines.append("")
            for item in provisions[:4]:
                response_lines.append(f"- {item}")

        if "critical_deadlines" in primary_doc:
            deadlines = primary_doc["critical_deadlines"]
            response_lines.append(f"\nImportant time limit: {deadlines.get('intimation_period', 'Immediate')}")

        if "statutory_timeline" in primary_doc:
            response_lines.append(f"\nExpected resolution time: {primary_doc['statutory_timeline']}")

        citations = primary_doc.get("citations", []) or []
        if citations:
            response_lines.append(f"\nSource: {', '.join(citations)}")

        response_lines.append("\nWould you like the step-by-step process, or the documents needed for this?")
        return "\n".join(response_lines)