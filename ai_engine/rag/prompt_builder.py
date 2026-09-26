"""
System prompt templates and context formatting for multilingual cooperative reasoning.
"""
from typing import List, Dict, Any

class PromptBuilder:
    SYSTEM_PROMPT = """You are an expert AI Legal & Governance Assistant for India's Cooperative Societies, Farmers, Primary Agricultural Credit Societies (PACS), and Rural Citizens under the Ministry of Cooperation.

Your mandate:
1. Provide accurate, legal, statutory, and procedural guidance on Multi-State Cooperative Societies Act, State Cooperative Bylaws, PMFBY (Crop Insurance), PM-KISAN, KCC, and PACS services.
2. If the user expresses a complaint or issue, act as a Resolution Navigator: provide the designated primary officer, exact documents needed, step-by-step escalation hierarchy, and statutory resolution timeline.
3. Always cite official acts, gazette notifications, or scheme guidelines.
4. Keep the tone empathetic, clear, structured, and easy for rural citizens to understand.
5. Answer strictly using the CONTEXT INFORMATION provided below, between the CONTEXT START and CONTEXT END markers. Do not add any fact, number, date, month, name, or citation that is not explicitly present in that context — not even ones you believe are true. If a detail isn't in the context, say "This specific detail isn't in our verified records" instead of guessing.
6. If a CONCERNED AUTHORITY section is provided below, include that officer's name and contact details in your answer exactly as given. If it says the district/block is needed, ask the user for their district and block instead of naming any officer. Never invent an officer name, phone number, or email that isn't explicitly given to you.
"""

    @classmethod
    def _format_authority(cls, authority: Dict[str, Any]) -> str:
        status = authority.get("status")
        designation = authority.get("designation", "the concerned officer")

        if status == "found":
            parts = [f"Designation: {designation}", f"Name: {authority.get('name')}"]
            if authority.get("district"):
                loc = authority["district"]
                if authority.get("block_name"):
                    loc += f" / {authority['block_name']}"
                parts.append(f"Location: {loc}")
            if authority.get("mobile"):
                parts.append(f"Mobile: {authority['mobile']}")
            if authority.get("landline"):
                parts.append(f"Landline: {authority['landline']}")
            if authority.get("email"):
                parts.append(f"Email: {authority['email']}")
            return " | ".join(parts)

        if status == "need_location":
            return f"Designation: {designation} | Contact not resolved: user's district/block was not mentioned in the query. Ask the user for their district and block."

        if status == "not_found_in_directory":
            return f"Designation: {designation} | {authority.get('note', 'No record found in our directory for this location yet.')}"

        return ""

    @classmethod
    def build_rag_prompt(cls, query: str, context_docs: List[Dict[str, Any]], language: str = "en",
                          authorities: List[Dict[str, Any]] = None) -> str:
        formatted_context = ""
        for i, doc in enumerate(context_docs, 1):
            title = doc.get("title") or doc.get("scheme_name") or doc.get("act_name") or "Document"
            summary = doc.get("summary") or doc.get("overview") or doc.get("financial_benefit") or ""
            provisions = doc.get("key_provisions") or doc.get("eligibility_criteria") or doc.get("permitted_activities") or []
            citations = doc.get("citations", [])

            formatted_context += f"\n--- Context Document {i}: {title} ---\n"
            formatted_context += f"Summary/Benefit: {summary}\n"
            if provisions:
                formatted_context += f"Details: {', '.join(provisions[:4])}\n"
            if citations:
                formatted_context += f"Official Citations: {', '.join(citations)}\n"

        formatted_authorities = ""
        if authorities:
            for a in authorities:
                line = cls._format_authority(a)
                if line:
                    formatted_authorities += f"- {line}\n"

        prompt = f"{cls.SYSTEM_PROMPT}\n\n"
        prompt += f"=== CONTEXT START ===\n{formatted_context}\n=== CONTEXT END ===\n\n"
        if formatted_authorities:
            prompt += f"CONCERNED AUTHORITY (use exactly as given, do not alter or invent):\n{formatted_authorities}\n\n"
        prompt += f"USER QUERY (Language requested: {language}):\n{query}\n\n"
        prompt += "Provide a complete, structured response with Key Points, Recommended Action, and Official Citations. Every fact must be traceable to the CONTEXT above — do not include any date, month, number, or name absent from it."
        return prompt

    @classmethod
    def build_generate_prompt(cls, query: str, context_docs: List[Dict[str, Any]], language: str = "en",
                              domain: str = "general", authorities: List[Dict[str, Any]] = None) -> str:
        """
        Prompt for the RAG-assisted generation path. Unlike the strict verified-only
        prompt, this one lets the model answer *any* question: it grounds itself on the
        retrieved context when available, and otherwise uses sound general knowledge of
        Indian cooperative law & agriculture schemes — clearly flagging what is general
        guidance vs. a verified record. This is what lets a "What is a PACS?" or
        "How do I become a member?" question get a real answer.
        """
        formatted_context = ""
        for i, doc in enumerate(context_docs, 1):
            title = doc.get("title") or doc.get("scheme_name") or doc.get("act_name") or "Document"
            summary = doc.get("summary") or doc.get("overview") or doc.get("financial_benefit") or ""
            provisions = doc.get("key_provisions") or doc.get("eligibility_criteria") or doc.get("permitted_activities") or []
            citations = doc.get("citations", [])

            formatted_context += f"\n--- Context Document {i}: {title} ---\n"
            formatted_context += f"Summary/Benefit: {summary}\n"
            if provisions:
                formatted_context += f"Details: {', '.join(provisions[:4])}\n"
            if citations:
                formatted_context += f"Official Citations: {', '.join(citations)}\n"

        formatted_authorities = ""
        if authorities:
            for a in authorities:
                line = cls._format_authority(a)
                if line:
                    formatted_authorities += f"- {line}\n"

        prompt = (
            "You are an expert AI Legal & Governance Assistant for India's Cooperative Societies, Farmers, "
            "PACS, and Rural Citizens under the Ministry of Cooperation.\n\n"
            "CONTEXT START\n"
            f"{formatted_context}"
            "CONTEXT END\n\n"
            "Instructions:\n"
            "1. Answer the user's question completely and helpfully. If it is a cooperative / agriculture / "
            "scheme / grievance question, explain the process, eligibility, required documents and, where "
            "applicable, the officer to approach.\n"
            "2. Prefer facts found in the CONTEXT above. Where the CONTEXT is missing a detail the user asked "
            "for, you MAY use general knowledge of Indian cooperative law and government schemes — label such "
            "parts with '(General guidance — please confirm with your local PACS/ARCS)'.\n"
            "3. Never invent a specific officer's name, phone number, email, or a specific figure as official. "
            "If the CONTEXT or the CONCERNED AUTHORITY section provides them, use them exactly; otherwise "
            "suggest the local Assistant Registrar of Cooperative Societies (ARCS) or PACS Secretary.\n"
            "4. Write the ENTIRE response in the language whose ISO 639-1 code is '{language}', in its native "
            "script (official names/URLs may stay in English).\n"
            "5. Structure the answer with clear headings: Key Points, Recommended Action, and (if any) "
            "Official Citations.\n"
        )
        if formatted_authorities:
            prompt += f"\nCONCERNED AUTHORITY (use exactly as given, do not alter or invent):\n{formatted_authorities}\n"
        prompt += f"\nUSER QUERY:\n{query}\n"
        return prompt.format(query=query, language=language)

    @classmethod
    def build_greeting_prompt(cls, query: str, language: str = "en") -> str:
        return (
            "You are the Multilingual Cooperative Assistant for Indian farmers, cooperative societies and rural "
            "citizens. The user's message (language requested: {language}) is:\n\n{query}\n\n"
            "This is a greeting or a general assistive message. Respond warmly and briefly (2-4 sentences). "
            "Describe what you can help with: Cooperative Laws (MSCS Act), Government Subsidy Schemes, PMFBY crop "
            "insurance, Kisan Credit Card credit, PACS services and grievance redressal. Do NOT invent specific "
            "scheme amounts, numbers or dates. If the user thanked you, acknowledge politely; if they asked who you "
            "are, introduce yourself by name; if they asked what you can do or asked for help, point them to the "
            "topics above."
        ).format(query=query, language=language)
