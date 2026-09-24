"""
Tamil Nadu District Officer Contact Directory Extractor & Data Standardizer.
Extracts, structures, and validates officer directory datasets for Madurai, Theni, and Pudukkottai districts.
Generates:
- database/data/officers/tamil_nadu_district_officers.json
- database/data/officers/tamil_nadu_district_officers.csv
"""

import os
import sys
import json
import csv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFICERS_DIR = os.path.join(BASE_DIR, "database", "data", "officers")
os.makedirs(OFFICERS_DIR, exist_ok=True)

# 1. Theni District Officers
THENI_OFFICERS = [
    {"district": "Theni", "department": "Agriculture", "name": "Tmt. Balasaraswathi", "designation_or_role": "Joint Director (Agri) Theni", "mobile": "9080550197", "landline": "04546-251862", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Tmt.R.Valarmathi", "designation_or_role": "Deputy Director Of Agriculture /Pa To Collector (Agri)", "mobile": "9786068555", "landline": "", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Thiru. Rajasekar", "designation_or_role": "Deputy Director Of Agriculture (Goi & Ss)", "mobile": "8946075280", "landline": "", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Thiru. Nivesh (I/C)", "designation_or_role": "Assistant Director (Agri) Theni", "mobile": "8489152123", "landline": "04546-250506", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Thiru. P.Kannan", "designation_or_role": "Assistant Director (Agri) Andipatti", "mobile": "9786992751", "landline": "04546-292025", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Thiru. N.Pandi", "designation_or_role": "Assistant Director (Agri) Kadamalaigundu", "mobile": "9655675404", "landline": "04546-293435", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Thiru. Vijayapandian (I/C)", "designation_or_role": "Assistant Director (Agri) Uthamapalayam", "mobile": "9659262299", "landline": "04546-265265", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Tmt.Ambika (I/C)", "designation_or_role": "Assistant Director (Agri) Cumbum", "mobile": "9894385336", "landline": "04546-270737", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Thiru. A.Murugesan", "designation_or_role": "Assistant Director (Agri) Bodinayakanur", "mobile": "8637413337", "landline": "04546-283539", "email": ""},
    {"district": "Theni", "department": "Agriculture", "name": "Tmt.Madhumitha (I/C)", "designation_or_role": "Assistant Director (Agri) Periyakulam", "mobile": "7092451949", "landline": "", "email": ""},
    {"district": "Theni", "department": "Animal Husbandry", "name": "Dr.V.Girija, B.V.Sc.", "designation_or_role": "Regional Joint Director (Animal Husbandry), Theni", "mobile": "9445001122", "landline": "4546251124", "email": ""},
    {"district": "Theni", "department": "Animal Husbandry", "name": "Dr.S. Eswaran,B.V.Sc.", "designation_or_role": "Assistant Director of Animal Husbandry, Periyakulam", "mobile": "9442245055", "landline": "", "email": ""},
    {"district": "Theni", "department": "Animal Husbandry", "name": "Dr.S.BASKARAN B.V.Sc.", "designation_or_role": "Assistant Director of Animal Disease Intelligence Unit, Theni.", "mobile": "9944504029", "landline": "", "email": ""},
    {"district": "Theni", "department": "Animal Husbandry", "name": "Dr.Sukumar, B.V.Sc", "designation_or_role": "Deputy Director of Cattle Breeding and fodder Development Theni @ Andipatti", "mobile": "9942933345", "landline": "", "email": ""},
    {"district": "Theni", "department": "Animal Husbandry", "name": "Dr.S.Kavitha, B.V.Sc", "designation_or_role": "Assistant Director Of Animal Husbandry,(I/C) Periyakulam", "mobile": "9442524088", "landline": "04546-233251", "email": ""},
    {"district": "Theni", "department": "Animal Husbandry", "name": "Dr.P.Sivarathina, B.V.Sc.", "designation_or_role": "Assistant Director of Animal Husbandry, Uthamapalayam", "mobile": "9842866632", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.P.Muthiah", "designation_or_role": "Cooperative SubRegistrar/ Secretary APCMS, Theni", "mobile": "9092121640", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Karuppadurai. K", "designation_or_role": "Cooperative SubRegistrar (Housing)", "mobile": "9629735321", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.K. Karuppathurai", "designation_or_role": "Cooperative Sub Registrar, Andipatti (Public Distribution Plan)", "mobile": "9629735321", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru. S.Rajaram", "designation_or_role": "Cooperative Sub Registrar, Cumbum (Public Distribution Plan)", "mobile": "9677433535", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Imayavaramban. S", "designation_or_role": "Cooperative Sub Registrar, Uthamapalayam (Public Distribution Plan)", "mobile": "8939841405", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.P.Sowndararajan", "designation_or_role": "Cooperative Sub Registrar, Bodinayakanur (Public Distribution Plan)", "mobile": "9786321374", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.P.Rajeskannan", "designation_or_role": "Cooperative Sub Registrar, Periyakulam (Public Distribution Plan)", "mobile": "8778336563", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru. V.Marisamy", "designation_or_role": "Cooperative Sub Registrar, Theni (Public Distribution Plan)", "mobile": "6383601716", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.A. Ganesan", "designation_or_role": "Cooperative Sub Registrar, Periyakulam", "mobile": "9750473510", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru. A.Baskara Pandian", "designation_or_role": "Cooperative Sub Registrar, Andipatti", "mobile": "7010357281", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru. R.Rameshkumar", "designation_or_role": "Cooperative Sub Registrar, Theni", "mobile": "9688920606", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "G. Sathish", "designation_or_role": "Cooperative Sub Registrar, Kadamalaigundu", "mobile": "9629701708", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Muniraja. K M", "designation_or_role": "Cooperative Sub Registrar, Bodinayakanur", "mobile": "9344507769", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.S. Imayavaramban", "designation_or_role": "Cooperative Sub Registrar, Chinnamanur", "mobile": "8939841405", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru. A. Anbu selvan", "designation_or_role": "Cooperative Sub Registrar, Cumbum", "mobile": "9486374714", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru.C.Ilangovan", "designation_or_role": "Cooperative Sub Registrar, Uthamapalayam", "mobile": "9994951934", "landline": "", "email": ""},
    {"district": "Theni", "department": "Co-operative", "name": "Thiru. T.Ramakritinan", "designation_or_role": "Cooperative Sub Registrar, Theni", "mobile": "9790017034", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Dr. R. Vaithinathan, I.A.S.", "designation_or_role": "District Collector", "mobile": "9444172000", "landline": "04546253676", "email": "collrthn@nic.in"},
    {"district": "Theni", "department": "District Administration", "name": "Thiru K.S Praveen Gowtham, IPS", "designation_or_role": "District Superintendent of police Theni.", "mobile": "9498233303", "landline": "04546254100", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru. P.Rajakumar", "designation_or_role": "District Revenue Officer", "mobile": "9445000917", "landline": "04546254946", "email": "dro.tnthn@nic.in"},
    {"district": "Theni", "department": "District Administration", "name": "Tmt.J.Kavitha (I/C)", "designation_or_role": "Revenue Divisional Officer, Periyakulam", "mobile": "9445000451", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru.M RAMAKRISHNAN", "designation_or_role": "Personal Assistant (General) to the Collector", "mobile": "9445008152", "landline": "4546-254956", "email": "pag.tnthn@nic.in"},
    {"district": "Theni", "department": "District Administration", "name": "Thiru.R.Sureshkumar", "designation_or_role": "District Backward And Minorities Welfare Officer", "mobile": "9445477841", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Tmt.J.Kavitha", "designation_or_role": "Special Deputy Collector, (Social Security Scheme)", "mobile": "7904632181", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru.K.Nallaiah", "designation_or_role": "District Supply Officer", "mobile": "9445000329", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Mr. G. Kiran, I.F.S.", "designation_or_role": "District Forest Officer", "mobile": "7708324267", "landline": "04546252552", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Tmt.S.Bharathi", "designation_or_role": "Personal Assistant To Collector (Accounts)", "mobile": "9363437015", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru.M.Kathirvel", "designation_or_role": "Additional Personal Assistant To Collector (Land)", "mobile": "9445008152", "landline": "4546-254956", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru.J.Ganga", "designation_or_role": "District Adi Dravidar And Tribal Welfare Officer", "mobile": "7338801273", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru.T.Panchapakesan", "designation_or_role": "Assistant Commissioner, Excise.", "mobile": "9003990146", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Mr. Vivek Kumar P. Yadav, I.F.S.", "designation_or_role": "Deputy Director, Srivilliputhur megamalai tiger reserve, Megamalai Division,Theni.", "mobile": "9442186292", "landline": "", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru L.Pandi", "designation_or_role": "PRO", "mobile": "9498042443", "landline": "4546-251997", "email": ""},
    {"district": "Theni", "department": "District Administration", "name": "Thiru. M.Syed Mohamed., B.A.", "designation_or_role": "Revenue Divisional Officer, Uthamapalyam", "mobile": "9445000452", "landline": "04546-231256", "email": "rdoupm.tnthn@nic.in"},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Rajat Beeton, IAS", "designation_or_role": "Additional Collector / Project Director (DRDA), Theni", "mobile": "7373704223", "landline": "04546254517", "email": "drdathn@nic.in"},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.S.Naveenkumar", "designation_or_role": "Camp Office Personal Assistant (PD to PC)", "mobile": "8838778352", "landline": "", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.M.Veerasamy", "designation_or_role": "Project Director,(TNSRLM),DMMU, Theni", "mobile": "9444094374", "landline": "04546255203", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Rajagopalan", "designation_or_role": "District Secretary (Panchayat), Theni", "mobile": "7402608015", "landline": "04546253674", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.A.Sundareshan", "designation_or_role": "Excutive Engineer", "mobile": "7373004583", "landline": "", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.G.Saminathan", "designation_or_role": "Block Development Officer (B.P)-Cumbum", "mobile": "7402608049", "landline": "04554274273", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Tmt .C.Nihilakumari", "designation_or_role": "Block Development Officer (B.pt)-Uthamapalayam", "mobile": "7402608045", "landline": "", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru. P.Andal", "designation_or_role": "Block Development Officer (B.P)-Chinnamanur", "mobile": "7402608041", "landline": "04554247376", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Jegadeeshchandra Bose", "designation_or_role": "Block Development Officer (B.pt)-Bodinaickanur", "mobile": "7402608037", "landline": "04546280218", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Jegadeesan", "designation_or_role": "Block Development Officer (B.P)-Periyakulam", "mobile": "7402608029", "landline": "04546231259", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Saravanan", "designation_or_role": "Block Development Officer (B.Pt)-Theni", "mobile": "7402608033", "landline": "04546252430", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.K.Saminathan", "designation_or_role": "Block Development Officer (V.P)-Chinnamanur", "mobile": "7402608042", "landline": "04554227260", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.S.Saravanan", "designation_or_role": "Block Development Officer (B.P)-Aundipatti", "mobile": "7402608021", "landline": "04546242325", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Tmt.Durgadevi", "designation_or_role": "Block Development Officer (V.P)-Cumbum", "mobile": "7402608050", "landline": "04554274273", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Tmt.A.Maithili", "designation_or_role": "Block Development Officer (V.pt)-Uthamapalayam", "mobile": "7402608046", "landline": "04554265238", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Tmt.T.Murugeshwari", "designation_or_role": "Block Development Officer (V.pt)Chinnamanur", "mobile": "7402608042", "landline": "04554247376", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Tmt.M.Makkaththammal", "designation_or_role": "Block Development Officer (V.P)-Bodinaickanur", "mobile": "7402608038", "landline": "04546280218", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Tmt.Bhuvaneshwari", "designation_or_role": "Block Development Officer (V.P)-Periyakulam", "mobile": "7402608030", "landline": "04546231259", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Ravichandran", "designation_or_role": "Block Development Officer (V.P)-Theni", "mobile": "7402608034", "landline": "04546252430", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.seetharaman", "designation_or_role": "Block Development Officer (V.Pt)-K.Myladumparai", "mobile": "7402608026", "landline": "04554227260", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru. D.Palanivel", "designation_or_role": "Assistant Director ( Panchayat)", "mobile": "7402608013", "landline": "04546262729", "email": "adp.tnthn@nic.in"},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.Annadurai", "designation_or_role": "PA to Collector ( Noon Meals)", "mobile": "7402608012", "landline": "4546260045", "email": ""},
    {"district": "Theni", "department": "DRDA", "name": "Thiru.vinothkumar", "designation_or_role": "Block Development Officer (B.pt)-Myladumparai", "mobile": "7402608025", "landline": "", "email": ""},
    {"district": "Theni", "department": "Education", "name": "திரு.அ.முருகன்", "designation_or_role": "Chief Educational Officer, Theni.", "mobile": "7373002957", "landline": "04546290244", "email": "ceo.tnthn@nic.in"},
    {"district": "Theni", "department": "Education", "name": "Thiru. R. PERUMALSAMY", "designation_or_role": "PERSONAL ASSISTANT (HS TO CEO), THENI.", "mobile": "9976624587", "landline": "4546290244", "email": ""},
    {"district": "Theni", "department": "Education", "name": "Tmt.D.Nagalakshmi", "designation_or_role": "District Educational Officer (Elementary), Theni. (Incharge)", "mobile": "7358802250", "landline": "4546266073", "email": ""},
    {"district": "Theni", "department": "Education", "name": "Thiru.Sanmugavel", "designation_or_role": "District Educational Officer (Private Schools), Theni.", "mobile": "9443771388", "landline": "4546260130", "email": ""},
    {"district": "Theni", "department": "Education", "name": "Thiru M.Surulivel", "designation_or_role": "District Educational Officer (Secondary), Theni.", "mobile": "7904183694", "landline": "4546232832", "email": ""},
    {"district": "Theni", "department": "Education", "name": "Thiru. T.Ragavan", "designation_or_role": "DEO Theni", "mobile": "9750982820", "landline": "04546260130", "email": ""},
    {"district": "Theni", "department": "Education", "name": "Thiru. V.Thirupathi", "designation_or_role": "District Education Officer,Uthamapalayam", "mobile": "7373002956", "landline": "04546266073", "email": "deopyk@nic.in"},
    {"district": "Theni", "department": "Education", "name": "Thiru. T.Balaji", "designation_or_role": "District Education Officer, Periyakulam", "mobile": "7373002953", "landline": "04546232832", "email": "deothn@nic.in"},
    {"district": "Theni", "department": "Fire & Rescue", "name": "Thiru.R.Balamurugan", "designation_or_role": "Asst.District Officer, Theni Allinagaram", "mobile": "9445086265", "landline": "", "email": "doth.tnfrs@gov.in"},
    {"district": "Theni", "department": "Fire & Rescue", "name": "Thiru. R. Kumaresan", "designation_or_role": "Asst.District Officer, Theni", "mobile": "", "landline": "04546-253657", "email": "doth.tnfrs@gov.in"},
    {"district": "Theni", "department": "Fire & Rescue", "name": "Thiru.R.Jegadeesh", "designation_or_role": "District Fire Officer, Theni", "mobile": "9445086265", "landline": "4546254100", "email": "doth.tnfrs@gov.in"},
    {"district": "Theni", "department": "Horticulture", "name": "Tmt.Nirmala", "designation_or_role": "Deputy Director (Horticulture) (i/c)", "mobile": "", "landline": "04546-255780", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Thiru. Needhinathan", "designation_or_role": "Assistant Director (Horti), Andipatti", "mobile": "8248490097", "landline": "4546-250245", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Tmt.A.Jasmine", "designation_or_role": "Assistant Director (Horti) Periyakulam", "mobile": "8940689196", "landline": "", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Thiru. K.Manikandan", "designation_or_role": "Assistant Director (Horti), Theni.", "mobile": "6383662003", "landline": "04546-250139", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Thiru.Arunkumar", "designation_or_role": "Assistant Director (Horti), Uthampalayam.", "mobile": "8940689196", "landline": "4554-232043", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Thiru.B.Rajamurugan", "designation_or_role": "Assistant Director (Horti), Bodinayakanur.", "mobile": "8072319001", "landline": "04546-284848", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Thiru R.C.Rajapriyadharsan", "designation_or_role": "Assistant Director (Horti), Cumbum.", "mobile": "7904724911", "landline": "04554275041", "email": ""},
    {"district": "Theni", "department": "Horticulture", "name": "Thiru. K.Karthik Raj", "designation_or_role": "Assistant Director (Horti), Chinnamanur.", "mobile": "9994742237", "landline": "04554246146", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.M.VARATHARAJAN", "designation_or_role": "District Health Officer, Theni", "mobile": "7358122675", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.S.MUTHUCHITRA", "designation_or_role": "Dean, Govt., Medical College & Hospital, Theni", "mobile": "9444249440", "landline": "04546263668", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.K.Kalai Selvi ,Mbbs", "designation_or_role": "Joint Director Of Health Services, Theni District", "mobile": "7358122083", "landline": "04546-232523", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.VIJAY ANAND", "designation_or_role": "MEDICAL COLLEGE SUPERINTENDENT", "mobile": "9842125935", "landline": "04546231292", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.SIVA KUMAR", "designation_or_role": "RMO", "mobile": "9443660668", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.K.S.KUMAR", "designation_or_role": "HOSPITAL SUPERINTENDENT -PKM", "mobile": "7010281374", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.ANBUCHEZHIYAN", "designation_or_role": "Deputy Director (Family Welfare).", "mobile": "7373232344", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.RAJAPRAKASH", "designation_or_role": "Deputy Director (Tuberculosis)", "mobile": "7358123298", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.RUBEN RAJ", "designation_or_role": "Deputy Director (Leprosy)", "mobile": "7358147176", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.GANAPATHY RAJESH", "designation_or_role": "District Programme Manager – District Blindness Control Society", "mobile": "9486046766", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.S.ANNAKAMU", "designation_or_role": "District Surveillance Medical Officer", "mobile": "8925589486", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.P.L.KARTHIK", "designation_or_role": "Epidemiologist", "mobile": "7358149338", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.MUTHU RUBHAN I/C", "designation_or_role": "Non-Communicable Diseases – District Programme Officer", "mobile": "7358148906", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.KAVIYA I/C", "designation_or_role": "National Health Mission", "mobile": "8489077561", "landline": "", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.S.RAVEENDRANATH", "designation_or_role": "Chief Medical Officer, Govt Hospital, Bodinayakanur", "mobile": "7358129227", "landline": "04546280232", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.M.Mohmmed Ali Jinnah", "designation_or_role": "Chief Medical Officer, Govt Hospital, Uthamapalayam", "mobile": "7358129381", "landline": "04554265243", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr. BANUMATHI", "designation_or_role": "Chief Medical Officer, Govt Hospital, Cumbum", "mobile": "7358129327", "landline": "04554271202", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr.MAHESHWARI", "designation_or_role": "Chief Medical Officer, Govt Hospital, Chinnamanur", "mobile": "7358129288", "landline": "04546246686", "email": ""},
    {"district": "Theni", "department": "Medical", "name": "Dr. Premalatha", "designation_or_role": "Chief Medical Officer, Govt Hospital, Andipatti", "mobile": "7358129288", "landline": "04546242600", "email": ""},
    {"district": "Theni", "department": "Municipality", "name": "Thiru.T Gopinath", "designation_or_role": "Commissioner, Chinnamanur", "mobile": "7397382181", "landline": "04554247383", "email": ""},
    {"district": "Theni", "department": "Municipality", "name": "Thiru.T.gopinath (I/C)", "designation_or_role": "Commissioner, Gudalur", "mobile": "7397382181", "landline": "04554231236", "email": ""},
    {"district": "Theni", "department": "Municipality", "name": "Thiru. D.Umashankar", "designation_or_role": "Commissioner, Cumbum", "mobile": "7397382183", "landline": "04554271283", "email": ""},
    {"district": "Theni", "department": "Municipality", "name": "Selvi.S.Parkavi", "designation_or_role": "Commissioner, Bodinayakanur", "mobile": "7397382185", "landline": "04546280228", "email": ""},
    {"district": "Theni", "department": "Municipality", "name": "Selvi.S.Thamiha Sulthana", "designation_or_role": "Commissioner, Periyakulam", "mobile": "7397382180", "landline": "04546231210", "email": ""},
    {"district": "Theni", "department": "Municipality", "name": "Thiru.P.Egraj", "designation_or_role": "Commissioner, Theni", "mobile": "7397382188", "landline": "04546252470", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru. M.Syed Mohamed., B.A.", "designation_or_role": "Revenue Divisional Officer, Uthamapalayam", "mobile": "9445000452", "landline": "04554265002", "email": "rdoupm.tnthn@nic.in"},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Kamalarajan", "designation_or_role": "Special Tahsildar Sipcot,", "mobile": "9443459496", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Ms. K. Sampoornam", "designation_or_role": "District Adidravidar and Tribal Welfare Officer", "mobile": "7338801273", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.S.Ravichandran", "designation_or_role": "Assistant Commissioner (Excise)", "mobile": "9865152079", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Tmt.J.Kavitha (I/C)", "designation_or_role": "Revenue Divisional Officer, Periyakulam", "mobile": "9445000451", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Mohan Muniyandi", "designation_or_role": "Taluk Supply Officer, Uthamapalayam", "mobile": "9445000333", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Kasinathan", "designation_or_role": "Taluk Supply Officer Aundipatti", "mobile": "9445000332", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Tmt.Ramaraj", "designation_or_role": "Taluk Supply Officer, Periyakulam.", "mobile": "9445000331", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Indra", "designation_or_role": "Taluk Supply Officer, Theni.", "mobile": "9445000330", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Suruli", "designation_or_role": "Tahsildar, Bodinayakanur.", "mobile": "9445000597", "landline": "04546-280124", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Balashanmugam", "designation_or_role": "Tahsildar, Uthamapalayam", "mobile": "9445000596", "landline": "04446-265226", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Tmt.Rathinam", "designation_or_role": "Tahsildar, Theni", "mobile": "9445000594", "landline": "4546-255133", "email": "tahsilthn.tnthn@nic.in"},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Sivakumar", "designation_or_role": "Taluk Supply Officer, Bodinayakanur", "mobile": "9445000334", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Senthilkumar", "designation_or_role": "Tahsildar, Andipatti", "mobile": "9445000595", "landline": "4546-290561", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Tmt. Bhuvaneshwari", "designation_or_role": "Tahsildar, Periyakulam", "mobile": "9445000593", "landline": "0454623215", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Mrs. P.Yasotha", "designation_or_role": "Special Tahsildar (SSS), Bodinayakanur", "mobile": "9488442231", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.Zahir Hussian", "designation_or_role": "Special Tahsildar (SSS), Uthampalayam", "mobile": "9944508958", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Thiru.S.Elango", "designation_or_role": "Special Tahsildar (SSS), Andipatti", "mobile": "9942052330", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Tmt.Uthayarani", "designation_or_role": "Special Tahsildar (SSS), Theni.", "mobile": "9865651902", "landline": "", "email": ""},
    {"district": "Theni", "department": "Revenue", "name": "Tmt.Pradeepa", "designation_or_role": "Special Tahsildar (SSS), Periyakulam", "mobile": "9843497676", "landline": "", "email": ""},
    {"district": "Theni", "department": "State Highways", "name": "Thiru.Elampooranam", "designation_or_role": "Assistant Divisional Engineer (SH), C&M, Uthamapalayam", "mobile": "9942946975", "landline": "", "email": ""},
    {"district": "Theni", "department": "State Highways", "name": "Thiru.Venkateshwaran", "designation_or_role": "Assistant Divisional Engineer (SH), C&M, Uthamapalayam", "mobile": "9500566322", "landline": "", "email": ""},
    {"district": "Theni", "department": "State Highways", "name": "Thiru.B.Muthukumar", "designation_or_role": "Assistant Divisional Engineer (SH), C&M, Periyakulam", "mobile": "9443404839", "landline": "", "email": ""},
    {"district": "Theni", "department": "State Highways", "name": "Thiru.V.Ramamoorthi", "designation_or_role": "Assistant Divisional Engineer (SH), C&M, Andipatti", "mobile": "9443558296", "landline": "", "email": ""},
    {"district": "Theni", "department": "State Highways", "name": "Thiru.P.K.Thirukumaran", "designation_or_role": "Assistant Divisional Engineer (SH), C&M, Theni", "mobile": "9791867989", "landline": "", "email": ""},
    {"district": "Theni", "department": "State Highways", "name": "Thiru.A.Kumanan", "designation_or_role": "Divisional Engineer (SH), C&M, Theni", "mobile": "9842144176", "landline": "", "email": ""},
    {"district": "Theni", "department": "TAHDCO", "name": "Thiru.M.Sundhararajan", "designation_or_role": "District Manager, TAHDCO", "mobile": "9445029480", "landline": "", "email": ""},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.D.Nadarajan", "designation_or_role": "SE-TNEB Theni", "mobile": "9443353670", "landline": "04546253677", "email": "setheni@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.V.Shanmuga", "designation_or_role": "Divisional Engineer, Theni", "mobile": "9445853171", "landline": "", "email": "eedtheni@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru. P.Balapoomi", "designation_or_role": "Divisional Engineer, Periyakulam", "mobile": "9445853177", "landline": "", "email": "eeperiakulam@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Chandramohan", "designation_or_role": "Divisional Engineer, Chinnamanur", "mobile": "9445853222", "landline": "", "email": "eechnmnr@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Senthilkumar", "designation_or_role": "Assistant Executive Engineer, Theni Town", "mobile": "9445853154", "landline": "4546253616", "email": ""},
    {"district": "Theni", "department": "TNEB", "name": "Thiru .Anandhan", "designation_or_role": "Assistant Executive Engineer, Dev & PRO", "mobile": "9445853139", "landline": "", "email": "protheni@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.V.Surulimuthu", "designation_or_role": "Assistant Executive Engineer, General", "mobile": "9445853138", "landline": "04546253616", "email": "aeegnlcotheni@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Prabu", "designation_or_role": "Excutive Engineer, Rural Theni", "mobile": "9445853160", "landline": "", "email": "mdt4763aee2@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Ravikumar", "designation_or_role": "Assistant Executive Engineer, Bodinayakanur, sub", "mobile": "9445853166", "landline": "", "email": "mdt4763aee3@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Prabu", "designation_or_role": "Assistant Executive Engineer, Rasingapuram sub", "mobile": "9445853153", "landline": "", "email": "mdt4763aee4@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Thangaraj", "designation_or_role": "Excutive Engineer , Civil", "mobile": "9445853144", "landline": "", "email": "aeeccotheni@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru. Parthasarathy", "designation_or_role": "Assistant Executive Engineer, East Periyakulam", "mobile": "9445853176", "landline": "", "email": "mdt4762aee1@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Muthuramalingam", "designation_or_role": "Assistant Executive Engineer, Periyakulam west", "mobile": "9445853183", "landline": "", "email": "mdt4762aee2@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Anandhan", "designation_or_role": "Assistant Executive Engineer ,GIS", "mobile": "9445853225", "landline": "", "email": "aeegistheni@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Murugan", "designation_or_role": "Assistant Executive Engineer, Andipatti west sub", "mobile": "9445853197", "landline": "", "email": "mdt4762aee4@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru. AlaghuRaja", "designation_or_role": "Assistant Executive Engineer, Chinnamanur sub", "mobile": "9445853204", "landline": "", "email": "mdt4761aee1@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Pandiyan", "designation_or_role": "Assistant Executive Engineer, Cumbum", "mobile": "9445853214", "landline": "", "email": "mdt4761aee4@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Rajmohan", "designation_or_role": "Assistant Executive Engineer, Uthamapalayam sub", "mobile": "9445853209", "landline": "", "email": "mdt4761aee3@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru. Jeyachandran", "designation_or_role": "Assistant Executive Engineer, Andipatti East", "mobile": "9445853189", "landline": "", "email": "mdt4762aee3@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.Saravanan", "designation_or_role": "Assistant Executive Engineer, kamachipuram sub", "mobile": "9445853221", "landline": "", "email": "mdt4761aee2@tnebnet.org"},
    {"district": "Theni", "department": "TNEB", "name": "Thiru.P.Prabu", "designation_or_role": "Assistant Executive Engineer, INFORMATION SYSTEM", "mobile": "9445853334", "landline": "", "email": "smtheni@tnebnet.org"},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru. K.Shanmugam", "designation_or_role": "Executive officer, Veerapandi", "mobile": "8925809679", "landline": "04546-246395", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Tmt.G.Umasundari", "designation_or_role": "Executive officer, Vadugapatti", "mobile": "8925809678", "landline": "04546-230161", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.M. Rajasekar", "designation_or_role": "Executive officer, Ganguvarpatti", "mobile": "8925809657", "landline": "04546-236566", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.K.Balasubramani", "designation_or_role": "Executive officer, Thevaram", "mobile": "8925809676", "landline": "04554-254616", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.D. Mohankumar", "designation_or_role": "Executive officer, Thenkarai", "mobile": "8925809675", "landline": "04546-230236", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.N. Alavanthar", "designation_or_role": "Executive officer, ThamaraiKulam", "mobile": "8925809674", "landline": "04546-230268", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.T. Yasotha", "designation_or_role": "Executive officer, C.Puthupatti", "mobile": "8925809673", "landline": "04554-270582", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.A. Basheer Ahamed", "designation_or_role": "Executive officer, Panaipuram", "mobile": "8925809672", "landline": "04554-252825", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Tmt. C. Yogasri (i/c)", "designation_or_role": "Executive officer Palani Chettipatti", "mobile": "8925809671", "landline": "04546-264998", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.V. Ganesan", "designation_or_role": "Executive office, Odaipatti", "mobile": "8925809670", "landline": "04546-247543", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.S. Elangovan", "designation_or_role": "Executive office, Melasokkanathapuram", "mobile": "8925809669", "landline": "04546-281991", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Tmt.K. Rokini", "designation_or_role": "Executive office, Markaiyankottai", "mobile": "8925809668", "landline": "04554-249331", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.R. Surulivel", "designation_or_role": "Executive officer, Kutchanur", "mobile": "8925809667", "landline": "04554-246199", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.R. Surulivel (i/c)", "designation_or_role": "Executive officer, Kompai", "mobile": "8925809661", "landline": "04554-252025", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru. S. Arumuganaenar", "designation_or_role": "Executive officer, Kamayakoundenpatti", "mobile": "8925809660", "landline": "04554-274144", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.G. Subaramanian", "designation_or_role": "Executive officer, Highwavis", "mobile": "8925809659", "landline": "04554-232225", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru.C. Murugan", "designation_or_role": "Executive officer, Hanumanthanpatti", "mobile": "8925809658", "landline": "04554-267904", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru. V. Ganesan", "designation_or_role": "Executive office, Genguvarpatti", "mobile": "7824058229", "landline": "04546236566", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Tmt. A. Vijaya", "designation_or_role": "Executive officer, Devathanapatti", "mobile": "8925809656", "landline": "04546-235530", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru. K. Sivakumar", "designation_or_role": "Executive officer, Boothipuram", "mobile": "8925809655", "landline": "04546264227", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Tmt.C. Yogasri", "designation_or_role": "Executive officer, B.Meenachipuram", "mobile": "8925809654", "landline": "04546-283620", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Tmt.A. Vijaya (i/c)", "designation_or_role": "Executive officer, Andipatti Jakkampatti", "mobile": "8925809653", "landline": "04546242324", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru. C. Rajaram", "designation_or_role": "Assistant Executive Engineer, Theni", "mobile": "8883100120", "landline": "04546265535", "email": ""},
    {"district": "Theni", "department": "Town Panchayat", "name": "Thiru. R. Muthukumar", "designation_or_role": "Assistant Director, Theni", "mobile": "7824058069", "landline": "04546265535", "email": ""}
]

# 2. Madurai District Officers
MADURAI_OFFICERS = [
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "District Collector", "mobile": "0452-2531110", "landline": "0452-2531110", "email": "collrmdu@nic.in"},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "District Revenue Officer", "mobile": "9445000916", "landline": "0452-2532106", "email": "dromdu@nic.in"},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "Joint Director (Kallar Reclamation)", "mobile": "", "landline": "0452-2532074", "email": ""},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "Personal Assistant to Collector (General)", "mobile": "9445008142", "landline": "0452-2533272", "email": "pagmdu@nic.in"},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "Spl. Deputy Collector (Social Security Scheme)", "mobile": "9445461741", "landline": "0452-2530513", "email": ""},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "District Supply Officer", "mobile": "9445000335", "landline": "0452-2546125", "email": "dso.mdu@tn.gov.in"},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "District Backward Class & Minorities Welfare Officer", "mobile": "9445477840", "landline": "0452-2529054", "email": ""},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "District Adi Dravida & Tribal Welfare Officer", "mobile": "", "landline": "0452-2536070", "email": ""},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "Assistant Commissioner (Excise)", "mobile": "", "landline": "0452-2531718", "email": ""},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "Assistant Director of Survey", "mobile": "", "landline": "0452-2525099", "email": "adsurmdu@nic.in"},
    {"district": "Madurai", "department": "Collectorate", "name": "", "designation_or_role": "Spl. Deputy Collector (Stamps)", "mobile": "", "landline": "0452-2521260", "email": ""},
    {"district": "Madurai", "department": "Revenue Division", "name": "", "designation_or_role": "Revenue Divisional Officer, Madurai", "mobile": "9445000449", "landline": "0452-2530644", "email": ""},
    {"district": "Madurai", "department": "Revenue Division", "name": "", "designation_or_role": "Revenue Divisional Officer, Usilampatti", "mobile": "9445000450", "landline": "04552-252149", "email": "rdo.usilampatti@tn.gov.in"},
    {"district": "Madurai", "department": "Revenue Division", "name": "", "designation_or_role": "Revenue Divisional Officer, Melur", "mobile": "9385251053", "landline": "0452-2422823", "email": ""},
    {"district": "Madurai", "department": "Revenue Division", "name": "", "designation_or_role": "Revenue Divisional Officer, Thirumangalam", "mobile": "9943110335", "landline": "04549-293933", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Tahsildar, Madurai North", "mobile": "9445000586", "landline": "0452-2532858", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Sathamangalam Zone", "mobile": "9384094350", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Koolapandi Zone", "mobile": "9384094351", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Tahsildar, Madurai West", "mobile": "9445461850", "landline": "0452-2605300", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Madurai West Zone", "mobile": "9384094352", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Tahsildar, Vadipatti", "mobile": "9445000589", "landline": "04543-254241", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Vadipatti Zone", "mobile": "9384094353", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Alanganallur Zone", "mobile": "9384094354", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Melur Zone", "mobile": "9384094355", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Kottampatti Zone", "mobile": "9384094356", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Madurai South Zone", "mobile": "9384094357", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Tahsildar, Madurai South", "mobile": "9445000587", "landline": "0452-2531645", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Madurai East Zone", "mobile": "9384094358", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Tahsildar, Thirupparankundram", "mobile": "9445461847", "landline": "0452-2482311", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Tirupparankundram Zone", "mobile": "9384094360", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Tirumangalam Zone", "mobile": "9384094359", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Kallikudi Zone", "mobile": "9384094361", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Usilampatti Zone", "mobile": "9384094362", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Chellampatti Zone", "mobile": "9384094363", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Taluk Office", "name": "", "designation_or_role": "Deputy Tahsildar Sedapatti Zone", "mobile": "9384094364", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Assistant Project Officer (Admin and Accounts), TNSRLM, Madurai", "mobile": "9444094129", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Assistant Account Officer, Madurai", "mobile": "", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Assistant Director(Lecture-1),T. Kallupatti", "mobile": "9384850192", "landline": "", "email": ""},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General), Madurai East", "mobile": "7402907037", "landline": "", "email": "bdo.maduraieast@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Madurai East", "mobile": "7402907039", "landline": "", "email": "bdo.maduraieast@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer (General) Madurai West", "mobile": "7402907046", "landline": "", "email": "bdo.maduraiwest@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Madurai West", "mobile": "7402907048", "landline": "", "email": "bdo.maduraiwest@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer (General), Thiruparankundram", "mobile": "7402907055", "landline": "", "email": "bdo.thirupparankundram@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Thiruparankundram", "mobile": "7402907057", "landline": "", "email": "bdo.thirupparankundram@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General), Thirumangalam", "mobile": "7402907126", "landline": "", "email": "bdo.thirumangalam@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Thirumangalam", "mobile": "7402907128", "landline": "", "email": "bdo.thirumangalam@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General), Alanganallur", "mobile": "7402907091", "landline": "", "email": "bdo.alanganallur@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Alanganallur", "mobile": "7402907093", "landline": "", "email": "bdo.alanganallur@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General), Vadipatti", "mobile": "7402907083", "landline": "", "email": "bdo.vadipatti@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Vadipatti", "mobile": "7402907085", "landline": "", "email": "bdo.vadipatti@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General),Melur", "mobile": "7402907067", "landline": "", "email": "bdo.melur@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Melur", "mobile": "7402907067", "landline": "", "email": "bdo.melur@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General), Kottampatti", "mobile": "7402907074", "landline": "", "email": "bdo.kottampatti@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(Panchayat), Kottampatti", "mobile": "7402907076", "landline": "", "email": "bdo.kottampatti@tn.gov.in"},
    {"district": "Madurai", "department": "Rural Development", "name": "", "designation_or_role": "Deputy Block Development Officer(General), Chellampatti", "mobile": "7402907108", "landline": "", "email": "bdo.chellampatti@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Tahsildar (C.S), Madurai North Taluk", "mobile": "9445000336", "landline": "", "email": "tsomdu.madurainorth@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Tahsildar (C.S), Madurai North Zone", "mobile": "9445000337", "landline": "", "email": "tsomdu.madurainz@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Tahsildar (C.S), Madurai Central Zone", "mobile": "9445000338", "landline": "", "email": "tsomdu.madurai_c@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Tahsildar (C.S), Madurai West Zone", "mobile": "9445000339", "landline": "", "email": "tsomdu.madurai_w@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Tahsildar (C.S), Madurai East Zone", "mobile": "9445000340", "landline": "", "email": "tsomdu.madurai_e@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Taluk Supply Officer, Melur", "mobile": "9445000341", "landline": "", "email": "tsomdu.melur@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Taluk Supply Officer, Vadipatti", "mobile": "9445000342", "landline": "", "email": "tsomdu.vadipatti@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Taluk Supply Officer, Usilampatti", "mobile": "9445000343", "landline": "", "email": "tsomdu.usilampatti@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Taluk Supply Officer, Thirumangalam", "mobile": "9445000344", "landline": "", "email": "tsomdu.thirumangalam@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Taluk Supply Officer, Peraiyur", "mobile": "9445000345", "landline": "", "email": "tsomdu.peraiyur@tn.gov.in"},
    {"district": "Madurai", "department": "Civil Supplies", "name": "", "designation_or_role": "Taluk Supply Officer - Kalligudi", "mobile": "7708502806", "landline": "", "email": ""}
]

# 3. Pudukkottai District Officers
PUDUKKOTTAI_OFFICERS = [
    # Page 1: District Officers, Police, Collectorate, Hospitals
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "District Collector", "place_or_address": "", "mobile": "", "landline": "04322-221663", "email": "collrpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "District Revenue Officer", "place_or_address": "", "mobile": "", "landline": "04322-220946", "email": "dro.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA(G) to Collector", "place_or_address": "", "mobile": "", "landline": "04322-221658", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA to Collector Land", "place_or_address": "", "mobile": "", "landline": "04322-221658", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA to Collector Accounts", "place_or_address": "", "mobile": "", "landline": "04322-221625", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA to Collector Small Savings", "place_or_address": "", "mobile": "6380206458", "landline": "04322-220347", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA to Collector Project Director", "place_or_address": "", "mobile": "7402607871", "landline": "04322-221691", "email": "adppdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA to Collector Noon Meal Program", "place_or_address": "", "mobile": "9443646861", "landline": "04322-222181", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "PA to Collector Agriculture", "place_or_address": "", "mobile": "9942135193", "landline": "04322-220245", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "District Officers", "name": "", "designation_or_role": "District Supply Office", "place_or_address": "", "mobile": "9445000311", "landline": "04322-221577", "email": "dso.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Police", "name": "", "designation_or_role": "Deputy Superintendent of Police Aranthangi", "place_or_address": "", "mobile": "9498100739", "landline": "04371-220562", "email": "dsp.aranthangi@tncctns.gov.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Police", "name": "", "designation_or_role": "Deputy Superintendent of Police Alangudi", "place_or_address": "", "mobile": "9498100764", "landline": "04322-251320", "email": "dsp.alangudi@tncctns.gov.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Police", "name": "", "designation_or_role": "Deputy Superintendent of Police Pudukkottai", "place_or_address": "", "mobile": "9498100731", "landline": "04322-222236", "email": "dsp.pudukkottai@tncctns.gov.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Police", "name": "", "designation_or_role": "Deputy Superintendent of Police Ponnamaravathi", "place_or_address": "", "mobile": "9498100755", "landline": "04333-262160", "email": "dsp.ponnamaravathy@tncctns.gov.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Police", "name": "", "designation_or_role": "Deputy Superintendent of Police Kottaipattinam", "place_or_address": "", "mobile": "9498100774", "landline": "04371-260350", "email": "dsp.kottaipattinam@tncctns.gov.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Police", "name": "", "designation_or_role": "Deputy Superintendent of Police Keeranur", "place_or_address": "", "mobile": "9498100746", "landline": "04339-262241", "email": "dsp.keeranur@tncctns.gov.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "Special Deputy Collector - Stamps", "place_or_address": "", "mobile": "9487257199", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "Reception Revenue Inspector", "place_or_address": "", "mobile": "9787548022", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "Hozur Sirasthar General", "place_or_address": "", "mobile": "9443807859", "landline": "04322-221624", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "Hozur Sirasthar Magistrate", "place_or_address": "", "mobile": "9943013755", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "H.S.(PD)", "place_or_address": "", "mobile": "9442170680", "landline": "04322-221691", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "Election Tahsildar", "place_or_address": "", "mobile": "7373757540", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "CABLE TV Tahsildar", "place_or_address": "", "mobile": "9498002582", "landline": "04322-230700", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "Public Relation Officer", "place_or_address": "", "mobile": "9498042438", "landline": "04322-221454", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Collectorate", "name": "", "designation_or_role": "District Supply Officer", "place_or_address": "", "mobile": "9445000311", "landline": "04322221626", "email": "dso.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Thirumayam", "place_or_address": "Thirumayam", "mobile": "", "landline": "04333-274222", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Karambakudi", "place_or_address": "Karambakudi", "mobile": "", "landline": "04322-258058", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Subramaniapuram", "place_or_address": "Subramaniapuram", "mobile": "", "landline": "04373-235450", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Avudaiyarkoil", "place_or_address": "Avudaiyarkoil", "mobile": "", "landline": "04371-233400", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Manamelgudi", "place_or_address": "Manamelgudi", "mobile": "", "landline": "04371-250010", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Keeranur", "place_or_address": "Keeranur", "mobile": "", "landline": "04339-262228", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Gandarvakottai", "place_or_address": "Gandarvakottai", "mobile": "", "landline": "04322-275669", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Valayapatti", "place_or_address": "Valayapatti", "mobile": "", "landline": "04333-262047", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Viralimalai", "place_or_address": "Viralimalai", "mobile": "", "landline": "04339-220200", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Hospitals", "name": "", "designation_or_role": "Government Hospital Illuppur", "place_or_address": "Illuppur", "mobile": "", "landline": "04339-272427", "email": "", "source": "Official Contact Directory"},

    # Page 2: Development, Revenue, Horticulture, Agricultural Engineering, Agri Marketing, Cooperation, School Education
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Avudaiyarkoil - Block Panchayat", "place_or_address": "Avudaiyarkoil", "mobile": "7402607844", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Avudaiyarkoil - Village Panchayat", "place_or_address": "Avudaiyarkoil", "mobile": "7402607845", "landline": "", "email": "pdkaukl.tnbdo@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Kunnandarkovil - Village Panchayat", "place_or_address": "Kunnandarkovil", "mobile": "7402607832", "landline": "04339246251", "email": "pdkknkl.tnbdo@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Kunnandarkovil - Block Panchayat", "place_or_address": "Kunnandarkovil", "mobile": "7402607831", "landline": "04333-246251", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Thiruvarankulam - Block Panchayat", "place_or_address": "Thiruvarankulam", "mobile": "7402607857", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Thiruvarankulam - Village Panchayat", "place_or_address": "Thiruvarankulam", "mobile": "7402607863", "landline": "", "email": "pdktklm.tnbdo@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Karambakudi - Village Panchayat", "place_or_address": "Karambakudi", "mobile": "9443784400", "landline": "", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Pudukkottai-Block Panchayat", "place_or_address": "Pudukkottai", "mobile": "9443150489", "landline": "04322-221805", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Pudukkottai - Village Panchayat", "place_or_address": "Pudukkottai", "mobile": "7402607842", "landline": "04322-221805", "email": "pdkpdki.tnbdo@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Development", "name": "", "designation_or_role": "Block Development Officer Arimalam - Block Panchayat", "place_or_address": "Arimalam", "mobile": "9442172512", "landline": "04333-271223", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Sub Collector Pudukkottai", "place_or_address": "Pudukkottai", "mobile": "9445000468", "landline": "04322-222219", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Revenue Divisional Officer Aranthangi", "place_or_address": "Aranthangi", "mobile": "9445000469", "landline": "04371-220589", "email": "rdoarg.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Revenue Divisional Officer Illupur", "place_or_address": "Illupur", "mobile": "9445461803", "landline": "04322-272049", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Pudukkottai", "place_or_address": "Pudukkottai", "mobile": "", "landline": "04322-221566", "email": "tahsilpdk.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Viralimalai", "place_or_address": "Viralimalai", "mobile": "", "landline": "04339-220777", "email": "", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Karambakkudi", "place_or_address": "Karambakkudi", "mobile": "", "landline": "04322-255199", "email": "tahsilkkd.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Ponnamaravathi", "place_or_address": "Ponnamaravathi", "mobile": "", "landline": "04333-260188", "email": "tahpon.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Thirumayam", "place_or_address": "Thirumayam", "mobile": "9445000643", "landline": "04322-274223", "email": "tahsiltym.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Manamelkudi", "place_or_address": "Manamelkudi", "mobile": "9445000646", "landline": "04371-250569", "email": "tahsilmnk.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Revenue", "name": "", "designation_or_role": "Tahsildar Avudaiyarkovil", "place_or_address": "Avudaiyarkovil", "mobile": "9445000645", "landline": "04371-233325", "email": "tahsilavk.tnpdk@nic.in", "source": "Official Contact Directory"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Deputy Director of Horticulture", "place_or_address": "Pudukkottai District", "mobile": "9788813286", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture (PM)", "place_or_address": "Pudukkottai", "mobile": "7094382390", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Pudukkottai", "mobile": "8144722116", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Kunnandarkoil", "mobile": "9344423902", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Gandarvakkottai", "mobile": "9944213234", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Thiruvarankulam", "mobile": "7904223804", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Karambakudi", "mobile": "9843917074", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Aranthangi", "mobile": "9659651859", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Viralimalai", "mobile": "9578770294", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Ponnamaravathi", "mobile": "9840232381", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Annavasal", "mobile": "9600016824", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Thirumayam", "mobile": "7299402881", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Arimalam", "mobile": "9786882155", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Avudayarkoil", "mobile": "9659651859", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Horticulture", "name": "", "designation_or_role": "Assistant Director of Horticulture", "place_or_address": "Manamelkudi", "mobile": "9659651859", "landline": "", "email": "", "source": "Official Horticulture page"},
    {"district": "Pudukkottai", "department": "Agricultural Engineering", "name": "", "designation_or_role": "Executive Engineer (Agricultural Engineering Department)", "place_or_address": "No. 81, Katupudukulam, Pudukkottai 622001", "mobile": "", "landline": "04322-221816", "email": "aedeepdk@tn.nic.in", "source": "Official Agricultural Engineering page"},
    {"district": "Pudukkottai", "department": "Agricultural Engineering", "name": "", "designation_or_role": "Assistant Executive Engineer (AE)", "place_or_address": "1426/C Trichy Main Road, near Highways office, Thirukokarnam Post, Pudukkottai 622002", "mobile": "", "landline": "", "email": "", "source": "Official Agricultural Engineering page"},
    {"district": "Pudukkottai", "department": "Agricultural Engineering", "name": "", "designation_or_role": "Assistant Executive Engineer (AE)", "place_or_address": "No.122, Rangojibava Street, Agraharam, Aranthangi 614616", "mobile": "", "landline": "", "email": "", "source": "Official Agricultural Engineering page"},
    {"district": "Pudukkottai", "department": "Agricultural Marketing & Agri Business", "name": "", "designation_or_role": "Deputy Director of Agriculture (Agri Business)", "place_or_address": "Pudukkottai", "mobile": "", "landline": "04322-221688", "email": "", "source": "Official Agricultural Marketing page"},
    {"district": "Pudukkottai", "department": "Co-operation, Food & Consumer Protection", "name": "", "designation_or_role": "Joint Registrar of Cooperative Societies", "place_or_address": "Pudukkottai Region", "mobile": "7338721500", "landline": "04322-236089", "email": "", "source": "Official Co-operation page"},
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "CHIEF EDUCATIONAL OFFICER, PUDUKKOTTAI", "place_or_address": "", "mobile": "9385229001 / 9385229002", "landline": "04322-222180", "email": "ceopdk@nic.in", "source": "Official School Education page"},

    # Page 3: School Education, Public Health, District Social Welfare, District Industries Centre
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "DISTRICT EDUCATION OFFICER, PUDUKKOTTAI", "place_or_address": "", "mobile": "9385229006", "landline": "04322-222510", "email": "deopdk@nic.in", "source": "Official School Education page"},
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "DISTRICT EDUCATION OFFICER, ARANTHANGI", "place_or_address": "", "mobile": "9385229007", "landline": "04371-223723", "email": "deoati@nic.in", "source": "Official School Education page"},
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "DISTRICT EDUCATION OFFICER, ILLUPPUR", "place_or_address": "", "mobile": "9385229008", "landline": "", "email": "", "source": "Official School Education page"},
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "DISTRICT PROJECT OFFICER, RASHTRIYA MADHYAMIK SHIKSHA ABHIYAN, PUDUKKOTTAI", "place_or_address": "", "mobile": "9385229003", "landline": "", "email": "", "source": "Official School Education page"},
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "DISTRICT PROJECT OFFICER, SARVA SHIKSHA ABHIYAN, PUDUKKOTTAI", "place_or_address": "", "mobile": "9788858835", "landline": "", "email": "", "source": "Official School Education page"},
    {"district": "Pudukkottai", "department": "School Education", "name": "", "designation_or_role": "DISTRICT INSPECTOR PHYSICAL EDUCATION, PUDUKKOTTAI", "place_or_address": "", "mobile": "9385229033", "landline": "", "email": "", "source": "Official School Education page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Deputy Director of Health Services", "place_or_address": "Pudukkottai", "mobile": "", "landline": "04322-221733", "email": "dphpdk@tn.nic.in", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Deputy Director of Health Services", "place_or_address": "Aranthangi", "mobile": "", "landline": "04371-220501", "email": "dphatg@tn.nic.in", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Pudukkottai Block", "mobile": "", "landline": "04322-293124", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Kunnandarkoil Block", "mobile": "", "landline": "04339-248309", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Annavasal Block", "mobile": "", "landline": "04339-241230", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Ponnamaravathy Block", "mobile": "", "landline": "04333-294994", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Thirumayam Block", "mobile": "", "landline": "04333-277276", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Viralimalai Block", "mobile": "", "landline": "04339-220484", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "Public Health & Preventive Medicine", "name": "", "designation_or_role": "Block Medical Officer", "place_or_address": "Arimalam Block", "mobile": "", "landline": "04333-272361", "email": "", "source": "Official Public Health page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "District Social Welfare Officer", "place_or_address": "District", "mobile": "", "landline": "04322-222270", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Annavasal Block", "mobile": "", "landline": "04339-230622", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Aranthangi Block", "mobile": "", "landline": "04371-220538", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Arimalam Block", "mobile": "", "landline": "04333-271223", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Avudyarkovil Block", "mobile": "", "landline": "04371-233323", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Gandarvakottai Block", "mobile": "", "landline": "04322-275728", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Karambakkudi Block", "mobile": "", "landline": "04322-255226", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Kunnandarkovil Block", "mobile": "", "landline": "04339-246251", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Manamelkudi Block", "mobile": "", "landline": "04371-250390", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Ponnmaravathi Block", "mobile": "", "landline": "04333-262070", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Pudukkottai Block", "mobile": "", "landline": "04322-221805", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Thiruvarankulam Block", "mobile": "", "landline": "04322-242281", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Thirumayam Block", "mobile": "", "landline": "04333-274227", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Social Welfare", "name": "", "designation_or_role": "Extension Officer (Social Welfare)", "place_or_address": "Viralimalai Block", "mobile": "", "landline": "04339-220224", "email": "", "source": "Official Social Welfare page"},
    {"district": "Pudukkottai", "department": "District Industries Centre", "name": "", "designation_or_role": "General Manager", "place_or_address": "Pudukkottai", "mobile": "", "landline": "04322-221794", "email": "", "source": "Official District Industries Centre page"}
]

def main():
    print("=" * 80)
    print("EXTRACTION & STANDARDIZATION OF TAMIL NADU DISTRICT OFFICER DIRECTORIES")
    print("=" * 80)

    all_officers = []
    
    # Process Theni
    for item in THENI_OFFICERS:
        entry = {
            "district": "Theni",
            "department": item["department"],
            "name": item.get("name", ""),
            "designation_or_role": item.get("designation_or_role", ""),
            "place_or_address": item.get("place_or_address", ""),
            "mobile": item.get("mobile", ""),
            "landline": item.get("landline", ""),
            "email": item.get("email", ""),
            "source": "https://theni.nic.in/contact_directory/"
        }
        all_officers.append(entry)
    print(f"✓ Extracted {len(THENI_OFFICERS)} officers for Theni District")

    # Process Madurai
    for item in MADURAI_OFFICERS:
        entry = {
            "district": "Madurai",
            "department": item["department"],
            "name": item.get("name", ""),
            "designation_or_role": item.get("designation_or_role", ""),
            "place_or_address": item.get("place_or_address", ""),
            "mobile": item.get("mobile", ""),
            "landline": item.get("landline", ""),
            "email": item.get("email", ""),
            "source": "https://madurai.nic.in/contact-directory/"
        }
        all_officers.append(entry)
    print(f"✓ Extracted {len(MADURAI_OFFICERS)} officers for Madurai District")

    # Process Pudukkottai
    for item in PUDUKKOTTAI_OFFICERS:
        entry = {
            "district": "Pudukkottai",
            "department": item["department"],
            "name": item.get("name", ""),
            "designation_or_role": item.get("designation_or_role", ""),
            "place_or_address": item.get("place_or_address", ""),
            "mobile": item.get("mobile", ""),
            "landline": item.get("landline", ""),
            "email": item.get("email", ""),
            "source": item.get("source", "https://pudukkottai.nic.in")
        }
        all_officers.append(entry)
    print(f"✓ Extracted {len(PUDUKKOTTAI_OFFICERS)} officers for Pudukkottai District")

    total_count = len(all_officers)
    print(f"\n★ TOTAL OFFICERS EXTRACTED ACROSS 3 DISTRICTS: {total_count}")

    # Write JSON Catalog
    json_path = os.path.join(OFFICERS_DIR, "tamil_nadu_district_officers.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_officers, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved JSON Catalog -> {json_path}")

    # Write CSV
    csv_path = os.path.join(OFFICERS_DIR, "tamil_nadu_district_officers.csv")
    fieldnames = ["district", "department", "name", "designation_or_role", "place_or_address", "mobile", "landline", "email", "source"]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_officers:
            writer.writerow(row)
    print(f"✓ Saved CSV Catalog  -> {csv_path}")

    # Write District Breakdown summary
    breakdown = {}
    for row in all_officers:
        d = row["district"]
        dept = row["department"]
        if d not in breakdown:
            breakdown[d] = {}
        breakdown[d][dept] = breakdown[d].get(dept, 0) + 1

    print("\n--- Summary Breakdown by Department ---")
    for d, depts in breakdown.items():
        print(f"\n📍 {d} District (Total: {sum(depts.values())} officers):")
        for dept, count in depts.items():
            print(f"   • {dept}: {count}")

    print("=" * 80)

if __name__ == "__main__":
    main()
