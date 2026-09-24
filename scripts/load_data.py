import os
import json
import sys

# Ensure stdout supports unicode on windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def validate_datasets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "database", "data")
    
    total_docs = 0
    print("[*] Validating Cooperative Knowledge Base Datasets...\n")
    
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    count = len(data) if isinstance(data, list) else 1
                    total_docs += count
                    rel_path = os.path.relpath(path, base_dir)
                    print(f"[OK] Verified [{count} records]: {rel_path}")

    print(f"\n[SUCCESS] Total verified documents loaded: {total_docs}")

if __name__ == "__main__":
    validate_datasets()

