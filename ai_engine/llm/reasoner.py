"""
LLM Reasoner with multi-backend support: Gemini, Groq, and Edge Rule-Grounded Synthesis.
Guarantees graceful degradation — when no external provider is reachable, the system
still produces grounded answers from the verified database (never fabricates facts).

The reasoner is language-aware: it instructs the model to respond *in the user's
language* so the final answer does not depend solely on a fragile translation step.
"""
import os
import re
from typing import Dict, Any, List, Optional

from config.settings import settings


class LLMReasoner:
    def __init__(self):
        self.provider = settings.DEFAULT_LLM_PROVIDER
        self.groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        self.gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")

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
        if self.gemini_key and self.provider == "gemini":
            answer = self._try_gemini(prompt, language)
            if answer:
                return answer
        if self.groq_key and self.provider == "groq":
            answer = self._try_groq(prompt, language)
            if answer:
                return answer

        # Edge synthesizer — grounded in the verified database, never hallucinates.
        return self._local_edge_reasoning(context_docs, domain, language)

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

    def _try_gemini(self, prompt: str, language: str) -> str:
        try:
            import httpx

            response = httpx.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
                params={"key": self.gemini_key},
                json={
                    "contents": [{"parts": [{"text": self._apply_language_instruction(prompt, language)}]}],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1500},
                },
                timeout=35.0,
            )
            response.raise_for_status()
            return self._parse_gemini(response.json())
        except Exception as exc:
            print(f"Gemini API call failed (falling back): {exc}")
            return ""

    def _try_groq(self, prompt: str, language: str) -> str:
        try:
            import httpx

            resp = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.groq_key}"},
                json={
                    "model": "openai/gpt-oss-120b",
                    "messages": [{"role": "user", "content": self._apply_language_instruction(prompt, language)}],
                    "temperature": 0.2,
                },
                timeout=20.0,
            )
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                return content.strip()
        except Exception as exc:
            print(f"Groq API call failed (falling back): {exc}")
        return ""

    def _local_edge_reasoning(self, docs: List[Dict[str, Any]], domain: str, language: str) -> str:
        if not docs:
            return (
                "I could not find a verified record matching your question in the official database. "
                "Please contact your local Assistant Registrar of Cooperative Societies (ARCS) or "
                "PACS Secretary with your full details, or rephrase and ask again."
            )

        primary_doc = docs[0]
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
        provisions = (
            primary_doc.get("key_provisions")
            or primary_doc.get("eligibility_criteria")
            or primary_doc.get("permitted_activities")
            or primary_doc.get("risk_coverage")
            or []
        )

        response_lines = [
            f"### 📌 {title}",
            f"\n**Overview & Guidance:**\n{summary}\n",
        ]

        if provisions:
            response_lines.append("**Key Provisions / Guidelines:**")
            for item in provisions[:4]:
                response_lines.append(f"- {item}")

        if "critical_deadlines" in primary_doc:
            deadlines = primary_doc["critical_deadlines"]
            response_lines.append(f"\n⚠️ **Mandatory Time Limits:** {deadlines.get('intimation_period', 'Immediate')}")

        if "statutory_timeline" in primary_doc:
            response_lines.append(f"\n⏱️ **Statutory Resolution Timeline:** {primary_doc['statutory_timeline']}")

        citations = primary_doc.get("citations", []) or []
        if citations:
            response_lines.append(f"\n🏛️ **Verified Legal Sources:** {', '.join(citations)}")

        return "\n".join(response_lines)