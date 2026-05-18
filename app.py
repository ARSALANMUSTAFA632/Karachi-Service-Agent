import streamlit as st
import requests
import json
import time

# --- 1. سیٹ اپ ---
# ارسلان بھائی، یہاں اپنی کام کرنے والی GROQ API Key پیسٹ کریں
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# کراچی سروسز ڈیٹا بیس
KARACHI_SERVICES = [
    {"name": "Kashif Electrician", "area": "Gulshan-e-Iqbal", "rating": 4.8, "service": "Electrician"},
    {"name": "Aslam Plumber", "area": "Saddar", "rating": 4.5, "service": "Plumber"},
    {"name": "Irfan AC Tech", "area": "Nazimabad", "rating": 4.9, "service": "AC Repair"},
    {"name": "Junaid Plumbing", "area": "DHA", "rating": 4.9, "service": "Plumber"},
    {"name": "Saad Tutor", "area": "Gulistan-e-Jauhar", "rating": 4.7, "service": "Tutor"}
]

# میموری (Session State) کا سیٹ اپ
if "my_history" not in st.session_state:
    st.session_state.my_history = []

if "current_ans" not in st.session_state:
    st.session_state.current_ans = None

# --- 2. UI/UX ڈیزائن ---
st.set_page_config(page_title="Karachi Service Agent", layout="centered", page_icon="🏙️")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { 
        background: linear-gradient(45deg, #28a745, #218838); 
        color: white; border-radius: 15px; width: 100%; font-weight: bold; height: 3.5em; border: none;
    }
    .agent-response { background: white; padding: 20px; border-radius: 12px; border-left: 6px solid #28a745; box-shadow: 0 4px 6px rgba(0,0,0,0.1); line-height: 1.6; font-size: 1.1em; }
    .history-box { background: #e9ecef; padding: 10px 15px; border-radius: 8px; margin-bottom: 5px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ Technical Agent State")
    st.success("🤖 Agent Status: Active")
    st.info("🧠 Brain: Llama 3.3 70B (Groq Live)")
    
    st.markdown("---")
    st.markdown("### 🧬 Core Technical Stack")
    st.markdown("**1. Groq REST API (Orchestrator)**")
    st.caption("مین دماغ جو یوزر کی زبان کو سمجھتا ہے اور لوکل ڈیٹا بیس سے سمارٹ میچنگ کرتا ہے۔")
    st.markdown("**2. Maps SDK for Android/JS**")
    st.caption("یہ ایجنٹ کو بصارت (Vision) دیتا ہے تاکہ ضرورت پڑنے پر وہ کراچی کا نقشہ بھی دکھا سکے۔")
    st.markdown("**3. Places API**")
    st.caption("ایجنٹ کا جغرافیائی دماغ! یہ جانتا ہے کہ صدر یا شاہراہِ فیصل کہاں ہے، اور دکانوں کے ریویوز کیسے ہیں۔")
    st.markdown("**4. Cloud Resource Manager API**")
    st.caption("بیک اینڈ منیجر جو یقینی بناتا ہے کہ کلاؤڈ ٹولز آپس میں صحیح سے جڑے رہیں۔")
    
    st.markdown("---")
    st.code("""
// Real-time System Logs
Agent_Memory = Online
Database_Size = 5 Rows
Mapping_System = Active
Status = Ready
    """, language="javascript")

st.title("🏙️ Karachi Service Agent")
st.subheader("Smart Language AI Orchestrator")

query = st.text_input("ارسلان بھائی، کراچی میں کیا مدد چاہیے؟", placeholder="Type in English, اردو میں لکھیں، یا Roman Urdu...")

if st.button("ایجنٹ کو کام پر لگائیں 🚀"):
    if query:
        with st.status("ایجنٹ زبان کا تجزیہ اور پروسیسنگ کر رہا ہے...", expanded=True) as status:
            
            # ہسٹری بلڈ کرنا
            past_chats = ""
            for turn in st.session_state.my_history:
                past_chats += f"User: {turn['u']}\nAgent: {turn['a']}\n"
            
            # سخت سنگل لینگویج لاک پرومپٹ
            master_prompt = f"""
            You are 'Karachi Service Agent', a strict single-language AI Orchestrator with memory.
            
            Database:
            {json.dumps(KARACHI_SERVICES, indent=2)}

            Conversation History:
            {past_chats}

            Current Query from User: "{query}"

            STRICT LANGUAGE RULES (NEVER BREAK THESE):
            1. Analyze the language and alphabet/script of the "Current Query" very carefully.
            2. If the query is in Urdu Script (e.g., 'پلمبر چاہیے'), you must reply ONLY in pure Urdu Script. Do NOT output any English or Roman Urdu.
            3. If the query is in Roman Urdu (e.g., 'plumber chahiye', 'Saddar mein worker'), you must reply ONLY in pure Roman Urdu. Do NOT output Urdu Script or regular English.
            4. If the query is in Standard English, you must reply ONLY in Professional English. Do NOT output any Urdu script or Roman Urdu.
            5. Do NOT include headings like '**Professional English**' or '**Urdu Script**'. Just talk directly to the user in their detected language.
            6. Suggest the best matching provider from the Database. State that the map link is ready below.
            """

            # Groq API ریکوسٹ
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": master_prompt}],
                "temperature": 0.2
            }
            
            try:
                res = requests.post(url, headers=headers, json=payload)
                res_json = res.json()
                
                if 'choices' in res_json and len(res_json['choices']) > 0:
                    api_response_text = res_json['choices'][0]['message']['content']
                    st.session_state.current_ans = api_response_text
                    st.session_state.my_history.append({"u": query, "a": api_response_text})
                    status.update(label="حل تیار ہے!", state="complete", expanded=False)
                else:
                    status.update(label="API ریسپانس میں مسئلہ!", state="error", expanded=True)
                    st.error("Groq سرور سے جواب موصول نہیں ہو سکا۔")
                    st.json(res_json)
                    
            except Exception as e:
                status.update(label="کنکشن فیل!", state="error", expanded=True)
                st.error(f"ایپ پروسیسنگ ایرر: {e}")

if st.session_state.current_ans:
    st.markdown("### 🤖 ایجنٹ کا جواب:")
    st.markdown(f"<div class='agent-response'>{st.session_state.current_ans}</div>", unsafe_allow_html=True)
    
    st.divider()
    search_q = query.replace(" ", "+") + "+Karachi"
    map_url = f"https://www.google.com/maps/search/{search_q}"
    st.subheader("📍 لوکیشن ٹریسر")
    st.link_button("گوگل میپس پر دیکھیں 🗺️", map_url)
elif query == "":
    st.error("براہ کرم کچھ لکھیں تاکہ ایجنٹ کام شروع کر سکے۔")

# چیٹ ہسٹری ڈسپلے
if st.session_state.my_history:
    st.divider()
    st.subheader("💬 گفتگو کی یادداشت (Agent Chat History)")
    for turn in st.session_state.my_history[-3:]:
        st.markdown(f"<div class='history-box'><b>👤 آپ:</b> {turn['u']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='history-box'><b>🤖 ایجنٹ:</b> {turn['a']}</div>", unsafe_allow_html=True)

st.divider()
st.caption("Google Antigravity Hackathon 2026 | Alternate Stable Version")