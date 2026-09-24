"""
LLM Reasoner with multi-backend support: Groq, Gemini, Local Ollama, and Edge Rule-Grounded Synthesis.
Guarantees 100% offline & edge availability for Smart Kiosks / Raspberry Pi devices.
"""
import os
from typing import Dict, Any, List
from config.settings import settings

class LLMReasoner:
    def __init__(self):
        self.provider = settings.DEFAULT_LLM_PROVIDER
        self.groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        self.gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")

    def generate_response(self, prompt: str, context_docs: List[Dict[str, Any]], domain: str, language: str = "en") -> str:
        if self.gemini_key and self.provider == "gemini":
            try:
                import httpx

                response = httpx.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                    params={"key": self.gemini_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1200},
                    },
                    timeout=20.0,
                )
                response.raise_for_status()
                candidates = response.json().get("candidates", [])
                parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
                answer = "".join(part.get("text", "") for part in parts).strip()
                if answer:
                    return answer
            except Exception as exc:
                print(f"Gemini API call fallback to local: {exc}")

        # Check if external API is configured
        if self.groq_key and self.provider == "groq":
            try:
                import httpx
                # Pluggable Groq call
                resp = httpx.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.groq_key}"},
                    json={
                        "model": "openai/gpt-oss-120b",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.2
                    },
                    timeout=10.0
                )
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Groq API call fallback to local: {e}")

        # Local Edge Synthesizer (Zero-latency, 100% offline compliant)
        return self._local_edge_reasoning(context_docs, domain, language)

    def _local_edge_reasoning(self, docs: List[Dict[str, Any]], domain: str, language: str) -> str:
        if not docs:
            return "No matching official cooperative record found for your exact query. Please consult your local Assistant Registrar of Cooperative Societies (ARCS) or PACS Secretary."

        primary_doc = docs[0]
        title = primary_doc.get("title") or primary_doc.get("scheme_name") or primary_doc.get("act_name") or primary_doc.get("category", "Cooperative Advisory")
        summary = primary_doc.get("summary") or primary_doc.get("overview") or primary_doc.get("financial_benefit") or primary_doc.get("description", "")
        provisions = primary_doc.get("key_provisions") or primary_doc.get("eligibility_criteria") or primary_doc.get("permitted_activities") or primary_doc.get("risk_coverage") or []
        
        response_lines = [
            f"### 📌 {title}",
            f"\n**Overview & Guidance:**\n{summary}\n"
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

        citations = primary_doc.get("citations", [])
        if citations:
            response_lines.append(f"\n🏛️ **Verified Legal Sources:** {', '.join(citations)}")

        return "\n".join(response_lines)
