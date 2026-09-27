"""
LLM-First Conversational Pipeline.

The LLM (Sarvam, then Groq) understands every query — language, intent, and follow-ups —
and writes the answer. Light-RAG retrieval is used only to GROUND the answer
with verified reference documents; catalog-heavy sub-model engines are no
longer part of the chat flow. Out of the box the assistant remains fully
multi-turn: it keeps the conversation history, replies in the user's language,
keeps answers plain for a farmer, and ends each turn with one follow-up question.
"""
import re
from typing import Dict, Any, List
from ai_engine.orchestration.domain_router import DomainRouter
from ai_engine.rag.prompt_builder import PromptBuilder
from ai_engine.llm.reasoner import LLMReasoner
from ai_engine.resolution_navigator.procedure_generator import ProcedureGenerator
from backend.app.services.speech_plan import build_speech_plan
from ai_engine.language.language_detector import LanguageDetector
from ai_engine.language.translation import TranslationEngine

class RAGPipeline:
    def __init__(self):
        self.router = DomainRouter()
        self.reasoner = LLMReasoner()
        self.lang_detector = LanguageDetector()
        self.translator = TranslationEngine()
        self.procedure_gen = ProcedureGenerator()

    def _answer_general(self, query: str, language: str) -> str:
        """Greeting / small-talk answered by the LLM directly in the user's language."""
        prompt = PromptBuilder.build_greeting_prompt(query, language)
        ans = self.reasoner.generate_response(prompt, [], "general", language)
        if (not ans or ans.strip().startswith("I could not find") or ans.strip().startswith("No matching official")):
            ans = self.reasoner.greeting_answer()
            if language and language != "en":
                translated = self.translator.translate(ans, "en", language)
                if translated:
                    ans = translated
        return ans.strip()

    def _no_record_message(self, language: str) -> str:
        msg = (
            "I could not find a verified official record matching your question in the database. "
            "Please rephrase your question or contact your local Assistant Registrar of Cooperative "
            "Societies (ARCS) or PACS Secretary with your full details."
        )
        if language and language != "en":
            translated = self.translator.translate(msg, "en", language)
            if translated:
                return translated
        return msg

    @staticmethod
    def _is_ascii(text: str) -> bool:
        if not text:
            return False
        printable = re.sub(r"\s+", "", text)
        if not printable:
            return False
        ascii_chars = sum(1 for ch in printable if ord(ch) < 128)
        return (ascii_chars / len(printable)) > 0.95

    # Script blocks for the Indic languages the assistant serves.
    _SCRIPT_RANGES = {
        "hi": (0x0900, 0x097F), "mr": (0x0900, 0x097F),
        "ta": (0x0B80, 0x0BFF), "te": (0x0C00, 0x0C7F), "kn": (0x0C80, 0x0CFF),
        "ml": (0x0D00, 0x0D7F), "bn": (0x0980, 0x09FF), "gu": (0x0A80, 0x0AFF),
        "pa": (0x0A00, 0x0A7F), "or": (0x0B00, 0x0B7F),
    }

    @staticmethod
    def _has_indic_script(text: str) -> bool:
        return any(
            any(RAGPipeline._SCRIPT_RANGES[code][0] <= ord(ch) <= RAGPipeline._SCRIPT_RANGES[code][1]
                for code in RAGPipeline._SCRIPT_RANGES)
            for ch in text
        )

    def _align_language(self, answer: str, language: str) -> str:
        """
        Indian LLMs sometimes answer in the wrong script. If the reply does not
        match the language the user is reading, translate it through the
        Bhashini -> Sarvam -> Google chain rather than showing the wrong script.
        """
        if not answer or not language:
            return answer
        lang = language.lower()
        indic_returned = self._has_indic_script(answer)
        if lang == "en" and indic_returned:
            translated = self.translator.translate(answer, "auto", "en")
            return translated.strip() if translated else answer
        if lang != "en" and self._is_ascii(answer):
            translated = self.translator.translate(answer, "en", lang)
            return translated.strip() if translated else answer
        return answer

    def process_query(self, query: str, language: str = "en", history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Auto-detect language from query text if Indic script characters are present
        if query and query.strip():
            det = self.lang_detector.detect(query)
            if det and det.get("language") and det.get("language") != "en":
                language = det.get("language")

        # 1. Light-RAG retrieval — grounding only, never the final answer.
        routing_result = self.router.route_and_retrieve(query=query, language=language)
        docs = routing_result.get("retrieved_context", [])[:4]
        citations = routing_result.get("citations", [])
        authorities = routing_result.get("authorities", [])
        primary_domain = routing_result["domain"]
        active_domains = routing_result.get("active_domains", [primary_domain])
        confidence = routing_result["intent"].get("confidence", 0.0)
        extracted_slots = routing_result.get("extracted_slots", {})

        # 2. Greetings (first turn only) — warm, short LLM reply.
        if self.reasoner.is_greeting(query) and not history:
            answer = self._answer_general(query, language)
            grounded = False
        else:
            # 3. LLM-first conversational generation: history + this turn, grounded
            #    on the retrieved reference documents, ending with a follow-up.
            system = PromptBuilder.build_assistant_system(language, docs, authorities=authorities)
            turns = (history or []) + [{"role": "user", "content": query}]
            answer = self.reasoner.chat(turns, system, language, docs)
            answer = (answer or "").strip()
            grounded = bool(docs)
            # An honest "I could not find a record" from the LLM is a real answer —
            # only fall back when every provider returned nothing at all.
            if not answer:
                answer = self._no_record_message(language)

        # 4. Make sure the reply is in the script the user is actually reading.
        answer = self._align_language(answer, language)

        # 5. Resolution procedure for complaints / redressal queries.
        procedure = None
        if any(w in query.lower() for w in ["complaint", "delay", "reject", "bribe", "refuse", "harass", "recover"]):
            procedure = self.procedure_gen.generate_for_query(query, docs)

        # 6. Decide the spoken part of the reply and the question to ask next.
        #    Done after the answer is final and language-aligned, so the voice
        #    reads exactly what the citizen can see.
        speech_plan = build_speech_plan(
            answer=answer,
            language=language,
            procedure=procedure,
            active_domains=active_domains,
        )

        return {
            "query": query,
            "language": language,
            "domain": primary_domain,
            "active_domains": active_domains,
            "is_multi_domain": len(active_domains) > 1,
            "confidence": confidence,
            "answer": answer,
            "recommended_officer": authorities[0] if authorities else None,
            "citations": list(dict.fromkeys(citations)),
            "verification_status": bool(grounded),
            "trust_score": 0.96 if grounded else 0.90,
            "verified_facts": [],
            "corrections_applied": [],
            "source_authority": citations[0] if citations else None,
            "procedure": procedure,
            "extracted_slots": extracted_slots,
            "authorities": authorities,
            "read_aloud": speech_plan["read_aloud"],
            "read_aloud_is_full": speech_plan["read_aloud_is_full"],
            "follow_up_kind": speech_plan["follow_up_kind"],
            "detail_withheld": speech_plan["detail_withheld"],
        }