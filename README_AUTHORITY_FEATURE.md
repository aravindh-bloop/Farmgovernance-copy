# Officer/Authority Recommendation Feature

## New file
- `ai_engine/retrieval/authority_lookup.py` — resolves a scheme's `designation`
  + your query text into a specific officer from `officer_directory.json`.

## Replace these files (same paths in your repo)
- `config/settings.py` — adds `OFFICER_DIRECTORY_PATH`
- `scripts/create_embeddings.py` — now carries `designation` into Chroma metadata
- `ai_engine/retrieval/vector_search.py` — now returns `designation` per result
- `ai_engine/retrieval/hybrid_retrieval.py` — now resolves officer contacts automatically
- `ai_engine/rag/prompt_builder.py` — now includes officer info in the LLM prompt
- `ai_engine/rag/rag_pipeline.py` — passes authorities through to the prompt

## Also drop in (from earlier steps)
- Your final `database/data/schemes/farmer_schemes.json` (45 schemes, with `designation`)
- Your `database/data/officers/officer_directory.json`

## Run after replacing
```bash
python scripts/create_embeddings.py
python -m backend.app.main
```

## What to expect right now
- Schemes with `designation: "AAO"` or `"ADA"` (Erode/Karur entries) will resolve
  to a real name/contact if you mention that district in your query.
- Other designations (District Collector/DRO, RDO/Tahsildar, DSO, DDA/JDA,
  Spl. Deputy Collector) will return "no record found in our directory yet" —
  because `officer_directory.json` still has long free-text designation values
  for those (e.g. "District Collector" as a separate entry from "District
  Revenue Officer"), not the exact combined string "District Collector / DRO".
  This isn't a bug in the new code — it'll resolve automatically once those
  values are normalized to match the 7 codes, whenever you're ready to do that.
- Not mentioning a district at all always returns a "please share your
  district" prompt — this is expected behavior, not an error.
