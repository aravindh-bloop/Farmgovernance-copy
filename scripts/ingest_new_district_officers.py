"""
Ingest newly uploaded district officers (Erode, Karur, Theni, Madurai) into standardized format
and merge into database/data/officers/tamil_nadu_district_officers.json & csv
"""

import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFICERS_JSON = os.path.join(BASE_DIR, "database", "data", "officers", "tamil_nadu_district_officers.json")
OFFICERS_CSV = os.path.join(BASE_DIR, "database", "data", "officers", "tamil_nadu_district_officers.csv")

# Load existing officers
existing_officers = []
if os.path.exists(OFFICERS_JSON):
    with open(OFFICERS_JSON, "r", encoding="utf-8") as f:
        existing_officers = json.load(f)

print(f"Initial officer count: {len(existing_officers)}")

# Newly uploaded data from PDF
NEW_DATA = [
    # ERODE
    {
        "id": "erode-001",
        "district": "Erode",
        "block_name": "Kodumudi",
        "head_quarters": "Vengambur",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "N.Nagarajan",
        "mobile": None,
        "landline": None,
        "email": None
    },
    {
        "id": "erode-002",
        "district": "Erode",
        "block_name": "Nambiyur",
        "head_quarters": "kadathur",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "MAIYARASU",
        "mobile": None,
        "landline": None,
        "email": None
    },
    {
        "id": "erode-003",
        "district": "Erode",
        "block_name": "Perundurai",
        "head_quarters": "THINGALURE",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "KALAISELVI",
        "mobile": None,
        "landline": None,
        "email": "kalaiagri95@gmail.com"
    },
    {
        "id": "erode-004",
        "district": "Erode",
        "block_name": "Bhavani",
        "head_quarters": "Bhavani 2",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "R.Dharmaraj",
        "mobile": None,
        "landline": None,
        "email": "sridharma22@gmail.com"
    },
    {
        "id": "erode-005",
        "district": "Erode",
        "block_name": "Chennimalai",
        "head_quarters": "Chennimalai",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "K.TAMILSELVI",
        "mobile": None,
        "landline": None,
        "email": "soillaberd@gmail.com"
    },
    {
        "id": "erode-006",
        "district": "Erode",
        "block_name": "Sathyamangalam",
        "head_quarters": "Kadambur",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "Manikandan",
        "mobile": None,
        "landline": None,
        "email": "suryamanimkd@gmail.com"
    },
    {
        "id": "erode-007",
        "district": "Erode",
        "block_name": "Anthiyur",
        "head_quarters": "Ennamangalam",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "K.NAVANEETHAN",
        "mobile": None,
        "landline": None,
        "email": None
    },
    {
        "id": "erode-008",
        "district": "Erode",
        "block_name": "Perundurai",
        "head_quarters": "SINGANALLUR",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "GOBINATH.M",
        "mobile": None,
        "landline": None,
        "email": None
    },
    {
        "id": "erode-009",
        "district": "Erode",
        "block_name": "Ammapettai",
        "head_quarters": "Kurichi",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "S.MUNIYAPPAN",
        "mobile": None,
        "landline": None,
        "email": "adaammapet@gmail.com"
    },
    {
        "id": "erode-010",
        "district": "Erode",
        "block_name": "Gobichettipalayam",
        "head_quarters": "Vellankovil",
        "department": "Agriculture",
        "designation": "AAO",
        "name": "K.JANARANJANI",
        "mobile": None,
        "landline": None,
        "email": "adagobi123@gmail.com"
    },

    # KARUR
    {
        "id": "karur-001",
        "district": "Karur",
        "block_name": "Kadavur",
        "head_quarters": "Kadavur",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "R.Ratnam",
        "mobile": None,
        "landline": None,
        "email": "rathupinju@gmail.com"
    },
    {
        "id": "karur-002",
        "district": "Karur",
        "block_name": "Karur",
        "head_quarters": "Karur",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "Manimekalai R",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.krr@gmail.com"
    },
    {
        "id": "karur-003",
        "district": "Karur",
        "block_name": "Thogaimalai",
        "head_quarters": "THOGAIMALAI",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "V.Madhan Kumar",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.tma@gmail.com"
    },
    {
        "id": "karur-004",
        "district": "Karur",
        "block_name": "Thanthoni",
        "head_quarters": "Thanthoni",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "S.Thangavel",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.tti@gmail.com"
    },
    {
        "id": "karur-005",
        "district": "Karur",
        "block_name": "Thanthoni",
        "head_quarters": "Thanthoni",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "R. Raju",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.tti@gmail.com"
    },
    {
        "id": "karur-006",
        "district": "Karur",
        "block_name": "Krishnarayapuram",
        "head_quarters": "Krishnarayapuram",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "S. Thangavel",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.krp@gmail.com"
    },
    {
        "id": "karur-007",
        "district": "Karur",
        "block_name": "Krishnarayapuram",
        "head_quarters": "Krishanarayapuram",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "S.Thangavel",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.krp@gmai.com"
    },
    {
        "id": "karur-008",
        "district": "Karur",
        "block_name": "Kulithalai",
        "head_quarters": "KULITHALAI",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "M ARAVINDAN",
        "mobile": None,
        "landline": None,
        "email": "aravind1971agri@gmail.com"
    },
    {
        "id": "karur-009",
        "district": "Karur",
        "block_name": "Thogaimalai",
        "head_quarters": "Sanarpatty",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "V Mathankumar",
        "mobile": None,
        "landline": None,
        "email": "atma.sanar@gmail.com"
    },
    {
        "id": "karur-010",
        "district": "Karur",
        "block_name": "Thanthoni",
        "head_quarters": "Thanthoni",
        "department": "Agriculture",
        "designation": "ADA",
        "name": "P.Parthiban",
        "mobile": None,
        "landline": None,
        "email": "adagriculture.tti2@gmail.com"
    },

    # THENI
    {
        "id": "theni-001",
        "district": "Theni",
        "block_name": "Theni",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Joint Director (Agri) Theni",
        "name": "Tmt. Balasaraswathi",
        "mobile": "9080550197",
        "landline": "04546-251862",
        "email": None
    },
    {
        "id": "theni-002",
        "district": "Theni",
        "block_name": None,
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Deputy Director Of Agriculture /Pa To Collector (Agri)",
        "name": "Tmt.R.Valarmathi",
        "mobile": "9786068555",
        "landline": None,
        "email": None
    },
    {
        "id": "theni-003",
        "district": "Theni",
        "block_name": None,
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Deputy Director Of Agriculture (Goi & Ss)",
        "name": "Thiru. Rajasekar",
        "mobile": "8946075280",
        "landline": None,
        "email": None
    },
    {
        "id": "theni-004",
        "district": "Theni",
        "block_name": "Theni",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Assistant Director (Agri) Theni",
        "name": "Thiru. Nivesh (I/C)",
        "mobile": "8489152123",
        "landline": "04546-250506",
        "email": None
    },
    {
        "id": "theni-005",
        "district": "Theni",
        "block_name": "Andipatti",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Assistant Director (Agri) Andipatti",
        "name": "Thiru. P.Kannan",
        "mobile": "9786992751",
        "landline": "04546-292025",
        "email": None
    },
    {
        "id": "theni-006",
        "district": "Theni",
        "block_name": "Kadamalaigundu",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Assistant Director (Agri) Kadamalaigundu",
        "name": "Thiru. N.Pandi",
        "mobile": "9655675404",
        "landline": "04546-293435",
        "email": None
    },
    {
        "id": "theni-007",
        "district": "Theni",
        "block_name": "Uthamapalayam",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Assistant Director (Agri) Uthamapalayam",
        "name": "Thiru. Vijayapandian (I/C)",
        "mobile": "9659262299",
        "landline": "04546-265265",
        "email": None
    },
    {
        "id": "theni-008",
        "district": "Theni",
        "block_name": "Cumbum",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Assistant Director (Agri) Cumbum",
        "name": "Tmt.Ambika (I/C)",
        "mobile": "9894385336",
        "landline": "04546-270737",
        "email": None
    },
    {
        "id": "theni-009",
        "district": "Theni",
        "block_name": "Bodinayakanur",
        "head_quarters": None,
        "department": "Agriculture",
        "designation": "Assistant Director (Agri) Bodinayakanur",
        "name": "Thiru. A.Murugesan",
        "mobile": "8637413337",
        "landline": "04546-283539",
        "email": None
    },

    # MADURAI
    {
        "id": "madurai-001",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "District Collector",
        "name": None,
        "mobile": "0452-2531110",
        "landline": "0452-2531110",
        "email": "collrmdu@nic.in"
    },
    {
        "id": "madurai-002",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "District Revenue Officer",
        "name": None,
        "mobile": "9445000916",
        "landline": "0452-2532106",
        "email": "dromdu@nic.in"
    },
    {
        "id": "madurai-003",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "Joint Director (Kallar Reclamation)",
        "name": None,
        "mobile": None,
        "landline": "0452-2532074",
        "email": None
    },
    {
        "id": "madurai-004",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "Personal Assistant to Collector (General)",
        "name": None,
        "mobile": "9445008142",
        "landline": "0452-2533272",
        "email": "pagmdu@nic.in"
    },
    {
        "id": "madurai-005",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "Spl. Deputy Collector (Social Security Scheme)",
        "name": None,
        "mobile": "9445461741",
        "landline": "0452-2530513",
        "email": None
    },
    {
        "id": "madurai-006",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "District Supply Officer",
        "name": None,
        "mobile": "9445000335",
        "landline": "0452-2546125",
        "email": "dso.mdu@tn.gov.in"
    },
    {
        "id": "madurai-007",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "District Backward Class & Minorities Welfare Officer",
        "name": None,
        "mobile": "9445477840",
        "landline": "0452-2529054",
        "email": None
    },
    {
        "id": "madurai-008",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "District Adi Dravida & Tribal Welfare Officer",
        "name": None,
        "mobile": None,
        "landline": "0452-2536070",
        "email": None
    },
    {
        "id": "madurai-009",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "Assistant Commissioner (Excise)",
        "name": None,
        "mobile": None,
        "landline": "0452-2531718",
        "email": None
    },
    {
        "id": "madurai-010",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "Assistant Director of Survey",
        "name": None,
        "mobile": None,
        "landline": "0452-2525099",
        "email": "adsurmdu@nic.in"
    },
    {
        "id": "madurai-011",
        "district": "Madurai",
        "block_name": None,
        "head_quarters": None,
        "department": "Collectorate",
        "designation": "Spl. Deputy Collector (Stamps)",
        "name": None,
        "mobile": None,
        "landline": "0452-2521260",
        "email": None
    },
    {
        "id": "madurai-012",
        "district": "Madurai",
        "block_name": "Madurai",
        "head_quarters": None,
        "department": "Revenue Division",
        "designation": "Revenue Divisional Officer, Madurai",
        "name": None,
        "mobile": "9445000449",
        "landline": "0452-2530644",
        "email": None
    },
    {
        "id": "madurai-013",
        "district": "Madurai",
        "block_name": "Usilampatti",
        "head_quarters": None,
        "department": "Revenue Division",
        "designation": "Revenue Divisional Officer, Usilampatti",
        "name": None,
        "mobile": "9445000450",
        "landline": "04552-252149",
        "email": "rdo.usilampatti@tn.gov.in"
    },
    {
        "id": "madurai-014",
        "district": "Madurai",
        "block_name": "Melur",
        "head_quarters": None,
        "department": "Revenue Division",
        "designation": "Revenue Divisional Officer, Melur",
        "name": None,
        "mobile": "9385251053",
        "landline": "0452-2422823",
        "email": None
    },
    {
        "id": "madurai-015",
        "district": "Madurai",
        "block_name": "Thirumangalam",
        "head_quarters": None,
        "department": "Revenue Division",
        "designation": "Revenue Divisional Officer, Thirumangalam",
        "name": None,
        "mobile": "9943110335",
        "landline": "04549-293933",
        "email": None
    },
    {
        "id": "madurai-016",
        "district": "Madurai",
        "block_name": "Madurai North",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Tahsildar, Madurai North",
        "name": None,
        "mobile": "9445000586",
        "landline": "0452-2532858",
        "email": None
    },
    {
        "id": "madurai-017",
        "district": "Madurai",
        "block_name": "Sathamangalam",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Sathamangalam Zone",
        "name": None,
        "mobile": "9384094350",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-018",
        "district": "Madurai",
        "block_name": "Koolapandi",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Koolapandi Zone",
        "name": None,
        "mobile": "9384094351",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-019",
        "district": "Madurai",
        "block_name": "Madurai West",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Tahsildar, Madurai West",
        "name": None,
        "mobile": "9445461850",
        "landline": "0452-2605300",
        "email": None
    },
    {
        "id": "madurai-020",
        "district": "Madurai",
        "block_name": "Madurai West",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Madurai West Zone",
        "name": None,
        "mobile": "9384094352",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-021",
        "district": "Madurai",
        "block_name": "Vadipatti",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Tahsildar, Vadipatti",
        "name": None,
        "mobile": "9445000589",
        "landline": "04543-254241",
        "email": None
    },
    {
        "id": "madurai-022",
        "district": "Madurai",
        "block_name": "Vadipatti",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Vadipatti Zone",
        "name": None,
        "mobile": "9384094353",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-023",
        "district": "Madurai",
        "block_name": "Alanganallur",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Alanganallur Zone",
        "name": None,
        "mobile": "9384094354",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-024",
        "district": "Madurai",
        "block_name": "Melur",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Melur Zone",
        "name": None,
        "mobile": "9384094355",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-025",
        "district": "Madurai",
        "block_name": "Kottampatti",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Kottampatti Zone",
        "name": None,
        "mobile": "9384094356",
        "landline": None,
        "email": None
    },
    {
        "id": "madurai-026",
        "district": "Madurai",
        "block_name": "Madurai South",
        "head_quarters": None,
        "department": "Taluk Office",
        "designation": "Deputy Tahsildar Madurai South Zone",
        "name": None,
        "mobile": "9384094357",
        "landline": None,
        "email": None
    }
]

# Standardize records to match master catalog schema
standardized_new = []
for item in NEW_DATA:
    district = item.get("district")
    dept = item.get("department")
    name = item.get("name") or ""
    designation = item.get("designation") or ""
    block = item.get("block_name") or ""
    hq = item.get("head_quarters") or ""
    mobile = item.get("mobile") or ""
    landline = item.get("landline") or ""
    email = item.get("email") or ""

    # Build detailed designation / role
    role_parts = [designation]
    if block and block.lower() not in designation.lower():
        role_parts.append(f"- {block}")
    if hq and hq.lower() not in designation.lower() and hq.lower() != block.lower():
        role_parts.append(f"({hq})")
    
    full_designation = " ".join(role_parts)

    place_parts = []
    if block:
        place_parts.append(block)
    if hq and hq != block:
        place_parts.append(hq)
    place_str = ", ".join(place_parts)

    source_url = f"https://{district.lower()}.nic.in"
    if district.lower() == "erode":
        source_url = "https://erode.nic.in/departments/agriculture/"
    elif district.lower() == "karur":
        source_url = "https://karur.nic.in/departments/agriculture/"
    elif district.lower() == "theni":
        source_url = "https://theni.nic.in/contact_directory/"
    elif district.lower() == "madurai":
        source_url = "https://madurai.nic.in/contact_directory/"

    record = {
        "id": item.get("id"),
        "district": district,
        "department": dept,
        "name": name,
        "designation_or_role": full_designation if (block or hq) else designation,
        "designation": designation,
        "block_name": block,
        "head_quarters": hq,
        "place_or_address": place_str,
        "mobile": str(mobile).strip() if mobile else "",
        "landline": str(landline).strip() if landline else "",
        "email": str(email).strip() if email else "",
        "source": source_url
    }
    standardized_new.append(record)

# Merge avoiding duplicates
def is_duplicate(r1, r2):
    if r1.get("district", "").lower() != r2.get("district", "").lower():
        return False
    # Check ID if available
    if r1.get("id") and r2.get("id") and r1.get("id") == r2.get("id"):
        return True
    # Match role + name or role + mobile
    role1 = (r1.get("designation_or_role") or r1.get("designation") or "").strip().lower()
    role2 = (r2.get("designation_or_role") or r2.get("designation") or "").strip().lower()
    name1 = (r1.get("name") or "").strip().lower()
    name2 = (r2.get("name") or "").strip().lower()
    mob1 = (r1.get("mobile") or "").strip().lower()
    mob2 = (r2.get("mobile") or "").strip().lower()
    
    if role1 and role1 == role2 and name1 and name1 == name2:
        return True
    if mob1 and mob2 and mob1 == mob2 and role1 == role2:
        return True
    return False

merged_list = list(existing_officers)
added_count = 0
for new_rec in standardized_new:
    found = False
    for idx, existing in enumerate(merged_list):
        if is_duplicate(existing, new_rec):
            # Update existing with any missing info (like email, block_name, id)
            for k, v in new_rec.items():
                if v and not existing.get(k):
                    existing[k] = v
            found = True
            break
    if not found:
        merged_list.append(new_rec)
        added_count += 1

print(f"Added {added_count} new officer records. Total records: {len(merged_list)}")

# Save JSON
with open(OFFICERS_JSON, "w", encoding="utf-8") as f:
    json.dump(merged_list, f, indent=2, ensure_ascii=False)

# Save CSV
fieldnames = ["district", "department", "name", "designation_or_role", "place_or_address", "block_name", "head_quarters", "mobile", "landline", "email", "source", "id"]
with open(OFFICERS_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in merged_list:
        writer.writerow(row)

print("Saved updated JSON and CSV successfully.")
