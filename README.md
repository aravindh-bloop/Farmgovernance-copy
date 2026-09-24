# 🌾 Multilingual Cooperative Governance & Legal Assistance Portal (SIH26088)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Languages](https://img.shields.io/badge/Indic_Languages-11_Supported-orange.svg)](https://bhashini.gov.in/)
[![Zero Hallucination](https://img.shields.io/badge/Zero--Hallucination-Verified_Gazettes-brightgreen.svg)](https://myscheme.gov.in)

> **Team BRAVITS** | **Smart India Hackathon 2026** | **Problem Statement ID:** `SIH26088`  
> **Theme:** Multilingual Cooperative Governance & Legal Assistance Chatbot

---

## 🌟 Overview

The **Multilingual Cooperative Governance & Legal Assistance Portal** is a zero-hallucination AI platform empowering 13+ Crore farmers, PACS secretaries, and rural citizens across **11 Indian languages**.

It delivers authenticated guidance on **Cooperative Laws**, **Ministry of Cooperation Schemes**, **PMFBY Crop Insurance**, **Financial Literacy (KCC)**, and **Grievance Resolution** across dual interfaces:
- 🖥️ **Smart Kiosk (`Port 5173`)**: Voice-first touchscreen interface for PACS rural offices.
- 🌐 **Web Portal (`Port 5174`)**: Modern responsive portal with real-time multi-domain guidance.

---

## 🚀 Quick Start: Local Hosting Guide

### 📋 Prerequisites
- **Python 3.10+** & **Node.js 18+** & **Git**

---

### 1️⃣ Clone & Setup Python Backend

```bash
# Clone the repository
git clone https://github.com/sathyasubha07/MULTILINGUAL-COOPERATIVE-ASSISTANT-CHATBOT-.git
cd MULTILINGUAL-COOPERATIVE-ASSISTANT-CHATBOT-

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install all Python dependencies
pip install -r requirements.txt
```

---

### 2️⃣ Install Frontend Dependencies

```bash
# Install Kiosk frontend dependencies
cd frontend && npm install && cd ..

# Install Web Portal dependencies
cd frontend-web && npm install && cd ..
```

---

### 3️⃣ Run All Services

#### 🔹 Option A: One-Click Launcher (Easiest)
- **Windows:** Double-click [`start_all.bat`](start_all.bat) or run `start_all.bat` in terminal.
- **Linux / macOS:** Run `chmod +x start_all.sh && ./start_all.sh`

#### 🔹 Option B: Run in Separate Terminals
1. **Backend API (`Port 8000`):**
   ```bash
   python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. **Kiosk Frontend (`Port 5173`):**
   ```bash
   cd frontend && npm run dev -- --host 0.0.0.0 --port 5173
   ```
3. **Web Portal (`Port 5174`):**
   ```bash
   cd frontend-web && npm run dev -- --host 0.0.0.0 --port 5174
   ```

---

## 🌐 Service Access URLs

| Service | Local URL | Description |
| :--- | :--- | :--- |
| **Backend API** | [http://localhost:8000](http://localhost:8000) | Core FastAPI AI engine |
| **API Swagger Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive API explorer |
| **Hardware Kiosk UI** | [http://localhost:5173](http://localhost:5173) | Touchscreen Kiosk interface |
| **Citizen Web Portal** | [http://localhost:5174](http://localhost:5174) | Full citizen & officer web portal |

---

## 🏛️ Core Domain Modules

| Domain Module | Key Topics & Coverage |
| :--- | :--- |
| **1. Cooperative Laws & By-laws** | MSCS Act 2002/2023 Amendments, State Acts, Sec 84 Arbitration, Sec 85 Ombudsman. |
| **2. Farmer Welfare Schemes** | 20+ schemes (MIDH, PM-KISAN, AIF, PM-KUSUM, SMAM, PKVY, NFSM) with seed collection points. |
| **3. PMFBY Crop Insurance** | 72-hour calamity intimation SLA, crop loss claims, toll-free `14447` routing. |
| **4. Financial Literacy** | KCC Scale of Finance calculation, 4% effective interest subvention, ₹1.60 Lakh collateral-free limit. |
| **5. Grievance Redressal** | 4-tier statutory escalation ladder, designated authority contact directory (`madurai.nic.in`, etc.). |

---

## 🗣️ Supported Indic Languages

| Code | Language | Script | Voice STT / TTS |
| :---: | :--- | :--- | :---: |
| `en` | English | English | ✅ Native |
| `hi` | Hindi | हिन्दी | ✅ Native |
| `ta` | Tamil | தமிழ் | ✅ Native Indic |
| `te` | Telugu | తెలుగు | ✅ Native Indic |
| `mr` | Marathi | मराठी | ✅ Native Indic |
| `kn` | Kannada | ಕನ್ನಡ | ✅ Native Indic |
| `bn` | Bengali | বাংলা | ✅ Native Indic |
| `gu` | Gujarati | ગુજરાતી | ✅ Native Indic |
| `ml` | Malayalam | മലയാളം | ✅ Native Indic |
| `pa` | Punjabi | ਪੰਜਾਬੀ | ✅ Native Indic |
| `or` | Odia | ଓଡ଼ିଆ | ✅ Native Indic |

---

## 🧪 Testing & Verification

```bash
# Run all domain verification test suites
python scripts/test_all_submodels.py

# Test live RAG pipeline
python scripts/demo_live_pipeline_output.py
```

---

## 📄 License
This project is licensed under the **MIT License**.
