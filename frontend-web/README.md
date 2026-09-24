# Multilingual Cooperative Assistant — Web Frontend (`frontend-web`)

> **IMPORTANT ARCHITECTURE NOTE:**
> This directory (`frontend-web`) contains the **web-facing frontend** application for the Multilingual Cooperative Assistant Chatbot.
> It is completely separate and independent from the touch-screen kiosk frontend located in the `/frontend` directory.
>
> - **Kiosk Frontend (`/frontend`):** Runs on port `5173` (Optimized for kiosk displays)
> - **Web Frontend (`/frontend-web`):** Runs on port `5174` (Optimized for desktop & mobile browsers)
>
> Both frontends connect to the same shared backend API endpoint (`http://localhost:8000/api/v1`).

---

## Features included in `frontend-web`

1. **Native Script Language Selection Screen**: Initial full-page language picker with native scripts (Tamil, Hindi, Kannada, Telugu, Marathi, Gujarati, Bengali, English).
2. **Modern Header & Branding**: Sleek top navbar with assistant branding, mode toggles, and navigation shortcuts.
3. **Unified Chat Interface**: Responsive chat bubble display, message history, typing indicators, text input, and mock voice input capability.
4. **Quick-Access Topic Cards**: Suggestion chips shown in empty state for instant query auto-filling.
5. **Downloadable Conversation**: Export chat transcript to PDF format directly from the browser using `jsPDF`.
6. **Dark / Light Theme & Text-Size Toggle**: Dark mode support and normal/large font accessibility scaling.
7. **Searchable FAQ Portal**: Interactive FAQ modal grouped by categories (Registration, Grievances, Schemes, PACS) with search filtering.
8. **Nearby Cooperative Office Locator**: Directory modal allowing district filtering with mock office details, contact numbers, and address listings.

---

## Getting Started

### Installation

```bash
cd frontend-web
npm install
```

### Running Locally

```bash
npm run dev
```
The application will start on **http://localhost:5174**.

### Build for Production

```bash
npm run build
```
