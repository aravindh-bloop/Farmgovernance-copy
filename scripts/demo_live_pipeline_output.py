"""
Comprehensive End-to-End Live Demonstration Script for Multilingual Cooperative Assistant.
Executes real queries through Intent Classification -> Multi-Domain Submodels -> Fusion Synthesizer -> Officer Recommender -> Database Cross-Verifier.
"""

import sys
import os
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ai_engine.rag.rag_pipeline import RAGPipeline

def main():
    print("=" * 85)
    print("🚀 MULTILINGUAL COOPERATIVE AI PORTAL - LIVE SYSTEM EXECUTION")
    print("   Repository: https://github.com/sathyasubha07/MULTILINGUAL-COOPERATIVE-ASSISTANT-CHATBOT- (main)")
    print("=" * 85)

    pipeline = RAGPipeline()

    demo_queries = [
        {
            "scenario": "SCENARIO 1: Multi-Domain Joint Solution + Verified Erode Officer Recommendation",
            "query": "Severe unseasonal rains flooded my paddy crop in Perundurai (Thingalure), Erode district, and the local PACS secretary is arbitrarily refusing my KCC loan. How do I appeal and who is the local agriculture officer?",
            "lang": "en"
        },
        {
            "scenario": "SCENARIO 2: Grievance Redressal & Anti-Overpricing Protocol + Theni Officer",
            "query": "PACS secretary in Cumbum, Theni is charging ₹350 per urea bag above MRP. Where can I lodge a statutory complaint with the local Sub Registrar?",
            "lang": "en"
        },
        {
            "scenario": "SCENARIO 3: Multilingual Tamil Query + Karur ADA Recommendation",
            "query": "கரூர் மாவட்டம் கடவூர் பகுதியில் PMFBY பயிர் காப்பீட்டு ஆலோசனை பெற உதவி வேளாண்மை இயக்குநர் (ADA) யார்?",
            "lang": "ta"
        },
        {
            "scenario": "SCENARIO 4: Financial Literacy (RBI Title Deed ₹5,000/Day Delay Penalty Rule)",
            "query": "Bank closed my KCC loan 40 days ago but has not returned my original property deed documents. What is the ₹5,000 per day compensation under RBI rules?",
            "lang": "en"
        },
        {
            "scenario": "SCENARIO 5: Cooperative Law (MSCS Act 2023 Sec 45 & Sec 84)",
            "query": "What are the rules for election under Section 45 and dispute arbitration under Section 84 of MSCS Act 2023?",
            "lang": "en"
        }
    ]

    for idx, item in enumerate(demo_queries, 1):
        print(f"\n{'=' * 85}")
        print(f"📌 [{idx}] {item['scenario']}")
        print(f"💬 Query: \"{item['query']}\" (Language: {item['lang']})")
        print(f"{'-' * 85}")

        res = pipeline.process_query(item["query"], item["lang"])
        
        print(f"🔹 Response Type       : {res.get('response_type')}")
        print(f"🔹 Active Domain Engines: {res.get('active_domains')}")
        print(f"🔹 Database Verification: {'🛡️ VERIFIED (Zero Hallucination)' if res.get('verification_status') else '⚠️ Unverified'}")
        print(f"🔹 Trust Score         : {int(res.get('trust_score', 0) * 100)}%")
        
        if res.get("verified_facts"):
            print(f"🔹 Verified Gazette Facts:")
            for fact in res.get("verified_facts"):
                print(f"   • {fact}")
                
        if res.get("citations"):
            print(f"🔹 Official Citations  : {res.get('citations')[:3]}")

        print(f"\n📖 GENERATED STATUTORY SOLUTION:\n")
        print(res.get("answer"))
        print(f"{'=' * 85}")

if __name__ == "__main__":
    main()
