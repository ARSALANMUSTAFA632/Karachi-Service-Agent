# 🏙️ Karachi Service Agent - Google Antigravity Hackathon Phase 2

## 🚀 Project Overview
Karachi Service Agent is an AI-driven Orchestrator designed to solve a hyper-local challenge: bridging the gap between Karachi's citizens and localized technical service providers (Electricians, Plumbers, AC Techs, Tutors) across changing language scripts. 

Built using Streamlit and powered by LLM orchestration, the core innovation lies in its strict **Single-Language Mirroring Engine**. The system dynamically detects the user's native input script (Urdu Script, Roman Urdu, or Standard English) and enforces a context-locked response mirroring that exact script, preserving cultural and geographic context without system cross-contamination.

---

## 🛠️ Architecture & Core Logic (Truthful Technical Blueprint)
To guarantee a 100% crash-proof deployment for Phase 2 evaluation under high-traffic conditions, the system is architected around two stable layers:

1. **State & Memory Management:** Utilizing Streamlit's `session_state` to anchor the `my_history` data structure. This prevents context loss during re-renders and compiles past chat logs to provide memory retention for the agent.
2. **Deterministic Prompt Injections:** Instead of forcing complex JSON structures from the LLM which frequently breach syntax limits, the system injects a structured database dictionary directly into the LLM runtime context alongside strict execution boundaries (`STRICT LANGUAGE RULES`).

---

## 🧬 Sidebar Telemetry & Enterprise Roadmap (Production Strategy)
The system UI explicitly outlines the **Core Technical Stack Blueprint** required for commercial scaling:
* **Structured Local Database:** Currently initialized via an in-memory micro-registry (`KARACHI_SERVICES`) to ensure immediate uptime during jury evaluation and eliminate external server latency.
* **Core LLM Engine Strategy (Groq & Llama Validation):** For this specific Phase 2 prototype, **Groq's REST API running Llama 3.3 70B** was utilized as the primary orchestrator to stress-test the Single-Language Mirroring logic under ultra-low latency. Because the entire application was built using Google's framework for **"Vibe Coding"**, the prompt structures and architecture are fully compatible and strategically mapped to be swapped with **Google Gemini 1.5 Pro / Flash** via Vertex AI in the final production deployment.
* **Cloud Resource Manager & Google Places API Roadmap:** Configured in the UI layout schema as a technical manifest to swap local entities with dynamic cloud clusters in Phase 3, allowing millions of rows of data to sync dynamically based on real-time user proximity in Karachi.
* **Maps SDK Mock-up:** The active link generation dynamically parses string parameters into clean web-mapping endpoints, serving as the interface framework for native Maps SDK integration in the production build.
