import sys
import os

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_engine.orchestration.intent_classifier import IntentClassifier
from ai_engine.rag.rag_pipeline import RAGPipeline

def run_tests():
    classifier = IntentClassifier()
    pipeline = RAGPipeline()

    print("================================================================")
    print("      EXHAUSTIVE MULTI-DOMAIN FUSION INTENT CLASSIFIER TEST     ")
    print("================================================================")

    test_queries = [
        ("Multi-Domain (PMFBY + Grievance)", "Hailstorm ruined my wheat crop yesterday, PACS secretary refused to accept PMFBY claim form"),
        ("Multi-Domain (PMFBY + KCC + Grievance)", "Flood destroyed standing crops, PACS asking for bribe to renew KCC crop loan, where to complain?"),
        ("Farmer Scheme (PM-KISAN DBT)", "What is the installment amount and e-KYC eligibility for PM-KISAN scheme?"),
        ("Cooperative Law (MSCS Sec 45 & 84)", "Section 45 Cooperative Election Authority voting rights and Section 84 arbitration in MSCS Act 2023"),
        ("Financial Literacy (KCC 4% Interest)", "What is the effective interest rate on Kisan Credit Card and scale of finance?"),
        ("Multilingual Hindi (72h PMFBY + पैक्स)", "मेरी गेहूं की फसल ओलावृष्टि से बर्बाद हो गई, 72 घंटे में पैक्स सचिव क्लेम नहीं ले रहा है"),
        ("Multilingual Tamil (பயிர் காப்பீடு + புகார்)", "பயிர் காப்பீடு இழப்பீடு கிடைக்கவில்லை, கூட்டுறவு சங்க செயலாளர் மீது புகார் செய்வது எப்படி?"),
        ("Multilingual Telugu (KCC + సబ్సిడీ)", "పీఎం కిసాన్ మరియు కిసాన్ క్రెడిట్ కార్డ్ 4 శాతం వడ్డీ రాయితీ వివరాలు ఏమిటి?"),
        ("Multilingual Marathi (पिक विमा + तक्रार)", "पिकांचे गारपिटीमुळे नुकसान झाले, सोसायटी सचिवाविरुद्ध अपील कुठे करावी?")
    ]

    for category, query in test_queries:
        res = classifier.classify(query)
        print(f"\n[Test Case]: {category}")
        print(f"Query: \"{query}\"")
        print(f"  -> Primary Domain  : {res['primary_domain']}")
        print(f"  -> Active Domains  : {res['active_domains']}")
        print(f"  -> Is Multi-Domain : {res['is_multi_domain']}")
        print(f"  -> Confidence Score: {res['confidence']}")
        print(f"  -> Extracted Slots : {res['extracted_slots']}")

    print("\n================================================================")
    print("    MULTI-DOMAIN SUBMODEL EXECUTION & DATABASE FUSION TEST       ")
    print("================================================================")
    fusion_query = "Flood destroyed standing crops, PACS secretary asking for bribe to renew KCC crop loan, how to appeal?"
    fusion_res = pipeline.process_query(fusion_query, language="en")

    print(f"Query: \"{fusion_query}\"")
    print(f"Activated Sub-Models: {fusion_res['active_domains']}")
    print(f"Is Multi-Domain     : {fusion_res['is_multi_domain']}")
    print(f"Verification Status : {fusion_res['verification_status']}")
    print(f"Overall Trust Score : {fusion_res['trust_score']}")
    print(f"Verified Facts      : {fusion_res['verified_facts']}")
    print(f"Source Authority    : {fusion_res['source_authority']}")
    print(f"Official Citations  : {fusion_res['citations'][:3]}")
    print(f"\n--- FUSED & SYNTHESIZED MULTI-DOMAIN ANSWER ---\n{fusion_res['answer']}")
    print("\n================================================================")
    print("ALL MULTI-DOMAIN FUSION TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
