"""
Builds a persistent ChromaDB vector index from the active domain knowledge files.
Run this once, and again any time the JSON content below changes:

    python scripts/create_embeddings.py

Each chunk's TITLE is embedded together with its content (not just the content
alone) — this matters because acronyms/scheme codes like "PM-KISAN" often only
appear in the title field, not in the body text. Without the title included,
a query for the exact scheme code can fail to match its own document.

Each scheme's "designation" field (the officer type responsible for it,
e.g. "AAO") is carried through into Chroma's metadata, so retrieval can
later look up the right contact via authority_lookup.py.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from sentence_transformers import SentenceTransformer
from config.settings import settings

COLLECTION_NAME = "cooperative_kb"

SOURCE_FILES = [
    os.path.join(settings.DATABASE_PATH, "schemes", "farmer_schemes.json"),
    os.path.join(settings.DATABASE_PATH, "financial", "financial_literacy.json"),
    os.path.join(settings.DATABASE_PATH, "grievances", "grievance_catalog.json"),
    os.path.join(settings.DATABASE_PATH, "pacs", "pacs_bylaws.json"),
    os.path.join(settings.DATABASE_PATH, "pmfby", "pmfby_guidelines.json"),
    os.path.join(settings.DATABASE_PATH, "laws", "cooperative_laws.json"),
]


def extract_doc_text(item):
    if "content" in item and item["content"]:
        return str(item["content"])
    parts = []
    # Primary textual fields
    for k in ["title", "scheme_name", "act_name", "grievance_type", "summary", "description", 
              "financial_benefit", "eligibility_criteria", "problem_statement", "statutory_remedy",
              "override_authority", "resolution_procedure", "penalty_on_violator", "application_mode_online", "application_mode_offline"]:
        if k in item and item[k]:
            parts.append(f"{k.replace('_', ' ').title()}: {str(item[k])}")
    # List fields
    for list_k in ["key_provisions", "key_benefits", "eligibility", "citations", "applicable_laws",
                  "documents_required", "formula_breakdown", "financial_mechanics", "required_evidence", "critical_deadlines"]:
        if list_k in item:
            val = item[list_k]
            if isinstance(val, list):
                parts.extend([str(x) for x in val if isinstance(x, (str, int, float))])
            elif isinstance(val, dict):
                for dk, dv in val.items():
                    parts.append(f"{dk}: {dv}")
    return " \n".join(parts) if parts else str(item)


def build_index():
    print(f"[*] Loading embedding model: {settings.EMBEDDING_MODEL}")
    model = SentenceTransformer(settings.EMBEDDING_MODEL)

    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(COLLECTION_NAME)

    ids, texts, metadatas = [], [], []
    for path in SOURCE_FILES:
        if not os.path.exists(path):
            print(f"[!] Skipping missing file: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
        for idx, item in enumerate(items):
            item_id = str(item.get("id") or f"{os.path.basename(path).split('.')[0]}_{idx}")
            title = str(item.get("title") or item.get("scheme_name") or item.get("act_name") or item.get("grievance_type") or item_id)
            content = str(item.get("content") or item.get("summary") or extract_doc_text(item) or "")
            domain = str(item.get("domain") or os.path.basename(path).split("_")[0])
            source = str(item.get("source") or (item.get("citations")[0] if item.get("citations") else ""))
            designation = str(item.get("designation") or "")

            scheme_code = str(item.get("scheme_code") or "")
            embed_text = f"{title}. {scheme_code}. {content}".strip()

            ids.append(item_id)
            texts.append(embed_text)
            metadatas.append({
                "domain": domain,
                "title": title,
                "source": source,
                "designation": designation,
            })
        print(f"[+] Loaded {len(items)} chunks from {os.path.relpath(path, settings.BASE_DIR)}")

    if not ids:
        print("[!] No documents found to embed. Check SOURCE_FILES paths.")
        return

    print(f"[*] Embedding {len(ids)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

    print(f"[OK] Indexed {len(ids)} documents into ChromaDB at {settings.VECTOR_DB_PATH}")


if __name__ == "__main__":
    build_index()
