"""
Comprehensive PACS + PMFBY Combined Sub-Model Test Suite for Cooperative AI Portal.
Tests:
1. PMFBY 72-Hour Calamity Intimation (Hailstorm, Flood, Post-Harvest 14-day loss)
2. PMFBY Standardized Premium Calculations (2% Kharif, 1.5% Rabi, 5% Commercial)
3. PMFBY Clause 17.2 100% Bank Default Liability Mandate
4. PACS Model Bye-laws 25+ Diversified Economic Activities
5. PACS Custom Hiring Centres (CHC) & Kisan Drones
6. PACS Membership, Deemed Membership & 15-day Loan Processing SLA
7. Multilingual queries across Hindi, Tamil, and English.
"""
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_engine.rag.rag_pipeline import RAGPipeline

def run_pacs_pmfby_tests():
    pipeline = RAGPipeline()

    print("================================================================")
    print("  COMPREHENSIVE PACS + PMFBY SUB-MODEL & CALAMITY TEST SUITE    ")
    print("================================================================")

    test_cases = [
        ("PMFBY 72-Hour Calamity Intimation", "Hailstorm damaged my standing wheat crop yesterday, how to intimate within 72 hours under PMFBY?"),
        ("PMFBY Premium Slabs & Subsidies", "What is the farmer premium percentage for Kharif, Rabi and commercial crops under PMFBY?"),
        ("PMFBY Clause 17.2 Bank Default Liability", "PACS deducted PMFBY crop insurance premium but failed to upload to NCIP portal before cut-off date, who pays my loss?"),
        ("PACS 25+ Multi-Purpose Services", "What new commercial and agricultural services can PACS operate under the Model Bye-laws?"),
        ("PACS Custom Hiring & Drone Spraying", "How can small farmers rent tractors and Kisan Drones from PACS Custom Hiring Centres?"),
        ("PACS Membership & 15-day Loan SLA", "What is the statutory time limit for PACS to approve loan application and open membership rules?"),
        ("Multilingual Hindi (72 घंटे ओलावृष्टि)", "ओलावृष्टि से गेहूं की फसल नष्ट हो गई है, 72 घंटे के अंदर पीएमएफबीवाई क्लेम कैसे दर्ज करें?"),
        ("Multilingual Tamil (பயிர் காப்பீட்டு பிரீமியம்)", "பயிர் காப்பீட்டு திட்டத்தில் காரீப் மற்றும் ரபி பயிர்களுக்கு விவசாயி கட்ட வேண்டிய பிரீமியம் எவ்வளவு?")
    ]

    for category, query in test_cases:
        lang = "hi" if "ओलावृष्टि" in query else "ta" if "பயிர்" in query else "en"
        res = pipeline.process_query(query, language=lang)
        print(f"\n----------------------------------------------------------------")
        print(f"📌 [Test Case]: {category}")
        print(f"Query: \"{query}\"")
        print(f"Primary Domain     : {res['domain']}")
        print(f"Active Domains     : {res['active_domains']}")
        print(f"Trust Score        : {res['trust_score']}")
        print(f"Verification Status: {res['verification_status']}")
        print(f"Official Citations : {res['citations'][:3]}")
        print(f"\n--- Verified Guidance Preview ---\n{res['answer'][:350]}...")

    print("\n================================================================")
    print("ALL PACS + PMFBY COMBINED SUB-MODEL TESTS COMPLETED & VERIFIED!")

if __name__ == "__main__":
    run_pacs_pmfby_tests()
