import streamlit as st
from datetime import date
import os

st.set_page_config(page_title="MediMate | Feel good, one step at a time", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#493d4e; --muted:#65596b; --plum:#71547d; --sage:#527568; }
.stApp { background:linear-gradient(135deg,#eee4d8 0%,#e9e3ee 52%,#deebe3 100%); color:var(--ink); }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
.stMarkdown, [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li, [data-testid="stCaptionContainer"],
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color:var(--ink) !important; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:#594765 !important; letter-spacing:-.03em; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#e9d9d0 0%,#e5ddef 55%,#d9e9df 100%); border-right:1px solid #d2c5d6; }
[data-testid="stSidebar"] > div:first-child { padding-top:1.4rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { color:#4d4055 !important; font-weight:700; padding:5px 0; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#594c60 !important; }
.hero { padding:2.2rem 2.4rem; border-radius:30px; background:linear-gradient(115deg,#eacbc5 0%,#ddd1e8 55%,#cfe2d6 100%); box-shadow:0 16px 38px #67526920; margin:0 0 1.5rem; }
.hero h1 { font-size:2.7rem; margin:0 0 .45rem; color:#503e58 !important; }
.hero p { color:#514657 !important; font-size:1.08rem; margin:0; }
.section-label { color:#71547d; text-transform:uppercase; letter-spacing:.13em; font-size:.78rem; font-weight:800; margin-bottom:.35rem; }
.fun-card { background:linear-gradient(135deg,#eee4d8 0%,#e9e0eb 100%); padding:1.4rem 1.5rem; border-radius:22px; border:1px solid #d6c9d9; box-shadow:0 8px 22px #55445c18; min-height:130px; margin-bottom:1rem; }
.fun-card h3 { font-size:1.15rem; margin:0 0 .5rem; }
.fun-card p { color:#53495a !important; margin:0; }
.small-note { background:#eadcbd; color:#594b36; border:1px solid #d9c8a6; border-radius:18px; padding:1rem 1.2rem; margin-top:1rem; }
[data-testid="stButton"] button { border:1px solid #cdbed3; border-radius:16px; background:linear-gradient(120deg,#e9d9d0 0%,#e6ddec 100%); color:#493d4e; font-weight:700; min-height:3rem; box-shadow:0 5px 14px #55445c14; transition:all .18s ease; }
[data-testid="stButton"] button:hover { border-color:#9e83aa; color:#60496c; transform:translateY(-2px); box-shadow:0 8px 20px #55445c22; }
[data-testid="stButton"] button p { color:#493d4e !important; }
[data-testid="stMetric"] { background:#e6ddd9; border:1px solid #d2c4d2; padding:1rem; border-radius:18px; }
[data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"] { color:#493d4e !important; }
[data-testid="stChatMessage"] { background:#e7dbd7; border:1px solid #d0c0ce; border-radius:18px; padding:.8rem 1rem; }
[data-testid="stChatMessage"]:nth-of-type(even) { background:#dce8df; }
[data-testid="stChatMessage"] * { color:#493d4e !important; }
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] textarea:focus { background:#e9dfd7 !important; color:#493d4e !important; border:1px solid #cdbed3; border-radius:16px; }
[data-testid="stChatInput"] textarea::placeholder { color:#716576 !important; }
[data-testid="stCheckbox"] label, [data-testid="stCheckbox"] label p { color:#493d4e !important; }
.stProgress > div > div > div > div { background:linear-gradient(90deg,#c98387,#9575a5,#719d83); }
div[data-baseweb="notification"] { color:#493d4e; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

PAGES = ["🏠 Home", "💬 Health Chat", "🌟 Healthy Habits", "🎯 Wellness Challenge", "ℹ️ About MediMate"]

def go_to(destination):
    st.session_state.page = destination


def open_prompt(prompt):
    answer = get_response(prompt, [{"role": "user", "content": prompt}])
    st.session_state.messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": answer},
    ]
    st.session_state.nav_page = "💬 Health Chat"


def get_response(question, conversation=None):
    """Use the AI service for open-ended answers, with safe offline topic replies."""
    text = " ".join(str(question).lower().strip().split())
    if not text:
        return "Type a question about sleep, food, exercise, feelings, or a common symptom and I'll try to help."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            api_key = None

    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
                instructions=(
                    "You are MediMate, a friendly, clear assistant. Answer the user's actual question "
                    "directly and stay relevant. You can answer safe questions on any topic, not only "
                    "health. Keep answers concise and explain unfamiliar terms. For health questions, "
                    "give general educational information only: do not diagnose, prescribe, or suggest "
                    "medicine doses. Encourage a trusted adult and qualified clinician for personal "
                    "medical concerns. If the user describes an emergency or immediate danger, tell "
                    "them to get help from a trusted adult and emergency services right away."
                ),
                input=conversation or [{"role": "user", "content": question}],
            )
            if response.output_text:
                return response.output_text.strip()
            return "I couldn't produce a reply just now. Please try asking again."
        except Exception:
            # Keep API keys and provider error details out of the visible chat.
            return "I couldn't reach the AI assistant just now. Please check your connection and API setup, then try again."

    def mentions(*terms):
        return any(term in text for term in terms)

    if mentions("thank you", "thanks", "thank u", "thx"):
        return "Your welcome and hope u will get better 🤩"
    if mentions("hello", "hi ", "hey", "good morning", "good evening"):
        return "Hi! 👋 I'm MediMate. Ask me about sleep, food, exercise, feelings, hygiene, or a common symptom. What would you like help with?"
    if mentions("can't breathe", "cannot breathe", "difficulty breathing", "trouble breathing", "chest pain", "passed out", "unconscious", "swallowed a", "overdose"):
        return "Please tell a trusted adult immediately and get urgent medical help. If you are in India and this is an emergency, call 112."
    if mentions("headache", "head hurts", "head pain", "migraine"):
        return "For a mild headache, try resting somewhere calm and drinking some water. Tell a trusted adult, especially if it is severe, sudden, keeps returning, or comes with other worrying symptoms."
    if mentions("sleep", "can't fall asleep", "cannot sleep", "insomnia", "bedtime", "tired"):
        return "A steady bedtime and a quiet wind-down can help. Try a calm activity before bed and keep screens away while settling down. Children aged 6–12 generally need 9–12 hours of sleep; teens aged 13–18 need 8–10 hours."
    if mentions("wash my hands", "washing hands", "wash hands", "handwashing", "clean my hands"):
        return "Wet your hands, add soap, and scrub your palms, backs of hands, between your fingers, and under your nails for about 20 seconds. Rinse well and dry them."
    if mentions("cough", "cold", "sore throat", "runny nose", "stuffy nose", "congestion"):
        return "Rest and fluids may help you feel more comfortable. Tell a trusted adult if you feel unwell. Get medical help promptly for trouble breathing, difficulty swallowing, or symptoms that are severe or getting worse."
    if mentions("fever", "temperature", "hot and shivery", "chills"):
        return "Tell a trusted adult so they can check how you are and decide whether you need medical care. Rest and drink fluids if you can. Get urgent help for trouble breathing, unusual difficulty waking, or other severe symptoms."
    if mentions("stomach", "tummy", "belly", "nausea", "feel sick", "throw up", "vomit", "diarrhea"):
        return "Tell a trusted adult how you feel. Rest and take small sips of water if you can. Seek medical help if pain is severe, you cannot keep fluids down, or you are getting worse."
    if mentions("cut", "scrape", "bleeding", "wound"):
        return "Tell a trusted adult. For a small cut, they can help rinse it with clean water and cover it with a clean dressing. Get medical help if bleeding will not stop or the injury is deep or serious."
    if mentions("burn", "scald"):
        return "Tell a trusted adult right away. Cool the burn under cool running water and get medical help for a large, deep, or very painful burn. Don't put ice, butter, or creams on it."
    if mentions("meditat", "mindful", "mindfulness", "breathing exercise", "calm down", "relax my mind"):
        return "Here's a gentle beginner meditation you can try for 2 minutes:\n\n1. Sit somewhere comfortable, with your feet supported. You can keep your eyes open or close them.\n2. Notice your breathing as it naturally goes in and out. You don't need to change it.\n3. When your mind wanders, that's normal. Gently bring your attention back to your next breath.\n4. When you're ready, notice the room around you and carry on with your day.\n\nIf focusing on your breath feels uncomfortable, stop and try noticing things you can see or hear instead. Meditation is for relaxation and isn't a substitute for help from a trusted adult or health professional."
    if mentions("stress", "stressed", "anxious", "anxiety", "worried", "nervous", "panic"):
        return "I'm sorry things feel stressful. Try a slow breath in and out, then name one small next step. Talking to someone you trust can help; if you feel unsafe or overwhelmed, tell an adult now."
    if mentions("sad", "lonely", "upset", "angry", "feelings", "mood"):
        return "Big feelings happen, and you don't have to handle them alone. Try telling someone you trust how you're feeling. If you might hurt yourself or don't feel safe, tell an adult immediately and get urgent help."
    if mentions("water", "hydration", "hydrated", "thirsty", "drink enough"):
        return "Keep water nearby and take regular sips, especially when you are active or it is hot. A trusted adult can help if you feel unwell or cannot drink."
    if mentions("breakfast", "lunch", "dinner", "snack", "food", "eat", "nutrition", "healthy meal"):
        return "A helpful meal can include a mix of foods you enjoy, such as fruit or vegetables, grains, and a source of protein. There is no single perfect meal—ask a trusted adult for options that suit you."
    if mentions("exercise", "workout", "fitness", "sport", "move", "active", "play"):
        return "Movement can be fun in lots of ways: walking, dancing, playing a game, stretching, or a sport you enjoy. Start gently and tell an adult if activity causes pain or makes you feel unwell."
    if mentions("teeth", "tooth", "brush", "dentist", "floss"):
        return "Brush gently with fluoride toothpaste in the morning and before bed. A trusted adult can help you choose a toothbrush and arrange regular dental checkups."
    if mentions("skin", "acne", "pimple", "spots"):
        return "Wash gently with mild soap and water, and avoid picking or squeezing spots. Skin changes are common; ask a trusted adult or healthcare professional if they are painful or worrying you."
    if mentions("habit", "healthy", "wellness", "feel better"):
        return "Try one small step today: drink some water, eat a variety of foods, move in a way you enjoy, get enough rest, or talk with someone you trust. Which area would you like a tip for?"
    return "I can answer common wellness questions while open-ended AI replies are not configured. For answers to other topics, set an OpenAI API key in the environment and restart MediMate. For medical concerns, please involve a trusted adult."


if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = PAGES[0]
if "nav_page" not in st.session_state:
    st.session_state.nav_page = st.session_state.page

with st.sidebar:
    st.markdown("<div style='font-size:2.6rem;text-align:center'>🌈</div><h2 style='text-align:center;margin:0'>MediMate</h2><p style='text-align:center'>Your little corner for feeling good</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:1px;background:#e9e1f1;margin:1.2rem 0'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Explore</div>", unsafe_allow_html=True)
    st.session_state.page = st.radio("Choose a page", PAGES, key="nav_page", label_visibility="collapsed")
    st.markdown("<div style='background:#e4d8e9;border:1px solid #cdbed3;border-radius:18px;padding:1rem;margin-top:1.2rem'><b style='color:#60496c'>A gentle reminder 💜</b><p style='font-size:.9rem;margin:.45rem 0 0'>Small steps count. Ask a trusted adult whenever you need help.</p></div>", unsafe_allow_html=True)

page = st.session_state.page

if page == "🏠 Home":
    st.markdown("<div class='hero'><div class='section-label'>A brighter day starts small</div><h1>Hey there, welcome to MediMate! 🌈</h1><p>Friendly, simple ideas for looking after yourself—one little step at a time.</p></div>", unsafe_allow_html=True)
    st.markdown("### What would you like to explore? ✨")
    prompts = ["What can help with a headache?", "How much sleep do kids need?", "How can I build healthy habits?", "How do I wash my hands well?"]
    cols = st.columns(2, gap="small")
    for index, prompt in enumerate(prompts):
        with cols[index % 2]:
            st.button(prompt, key=f"prompt_{index}", use_container_width=True, on_click=open_prompt, args=(prompt,))
    st.markdown('<div class="small-note">⭐ Tiny reminder: You do not have to be perfect to be healthy. One small positive choice is a great start!</div>', unsafe_allow_html=True)

elif page == "💬 Health Chat":
    st.markdown('<div class="section-label">Your friendly question corner</div>', unsafe_allow_html=True)
    st.title("💬 Chat with MediMate")
    st.write("Ask a general health question. If symptoms are severe or urgent, tell a trusted adult and seek medical help.")
    if not os.getenv("OPENAI_API_KEY"):
        try:
            api_key_configured = bool(st.secrets.get("OPENAI_API_KEY"))
        except Exception:
            api_key_configured = False
        if not api_key_configured:
            st.info("Open-ended answers are turned off until an OpenAI API key is configured. Set OPENAI_API_KEY in your environment, then restart MediMate.")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hiiii! 👋 I'm MediMate. Ask me about everyday wellness, sleep, hydration, common symptoms, or healthy habits!"}]
    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.caption("💜 Be curious. Be kind to yourself. Ask for adult help when needed.")
    with top_right:
        if st.button("🧹 Clear chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Fresh start! 🌈 What would you like to ask?"}]
            st.rerun()
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🌈" if message["role"] == "assistant" else "🙂"):
            st.markdown(message["content"])
    st.markdown("**Try asking:**")
    quick_cols = st.columns(3)
    quick_prompts = ["How can I sleep better?", "What should I do if I have a cough?", "How can I drink enough water?"]
    for i, prompt in enumerate(quick_prompts):
        with quick_cols[i]:
            if st.button(prompt, key=f"chatquick_{i}", use_container_width=True):
                updated_history = st.session_state.messages + [{"role": "user", "content": prompt}]
                answer = get_response(prompt, updated_history[-12:])
                st.session_state.messages.extend([
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": answer},
                ])
                st.rerun()
    user_input = st.chat_input("Type your question here... ✍️")
    if user_input:
        updated_history = st.session_state.messages + [{"role": "user", "content": user_input}]
        answer = get_response(user_input, updated_history[-12:])
        st.session_state.messages.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": answer},
        ])
        st.rerun()

elif page == "🌟 Healthy Habits":
    st.markdown('<div class="section-label">Power up your day</div>', unsafe_allow_html=True)
    st.title("🌟 Healthy habits")
    st.write("Healthy doesn't mean perfect. Try a few small things that work for you!")
    habits = [
        ("🥗", "Eat a variety", "Try different fruits, vegetables, grains, and other nourishing foods."),
        ("💧", "Sip water", "Drink regularly, especially when playing or when it's hot."),
        ("😴", "Get enough sleep", "A regular bedtime can help you feel rested and ready."),
        ("🏃", "Move and play", "Walking, dancing, sports, and games all count."),
        ("🧼", "Wash your hands", "Use soap and water before eating and after using the bathroom."),
        ("💜", "Check in with yourself", "Talk to someone you trust when feelings get big.")
    ]
    for start in range(0, len(habits), 2):
        cols = st.columns(2, gap="medium")
        for col, item in zip(cols, habits[start:start+2]):
            with col:
                st.markdown(f'<div class="fun-card"><h3>{item[0]} {item[1]}</h3><p>{item[2]}</p></div>', unsafe_allow_html=True)
    st.info("💡 Children aged 6–12 generally need about 9–12 hours of sleep each night. Needs can vary as you grow.", icon="🌙")

elif page == "🎯 Wellness Challenge":
    st.markdown('<div class="section-label">Little wins count</div>', unsafe_allow_html=True)
    st.title("🎯 Today's Wellness Challenge")
    st.write(f"Your friendly checklist for **{date.today().strftime('%A, %d %B')}**. No pressure—just do what you can!")
    challenge_items = [
        "💧 I drank water regularly",
        "🍎 I ate a variety of foods",
        "🏃 I moved, stretched, or played",
        "🧼 I washed my hands with soap",
        "💜 I took a calm break or talked to someone",
        "🌙 I made a plan for bedtime"
    ]
    if "challenge_date" not in st.session_state or st.session_state.challenge_date != str(date.today()):
        st.session_state.challenge_date = str(date.today())
        st.session_state.challenge_checks = {item: False for item in challenge_items}
    for item in challenge_items:
        st.session_state.challenge_checks[item] = st.checkbox(item, value=st.session_state.challenge_checks.get(item, False), key=f"check_{item}")
    completed = sum(st.session_state.challenge_checks.values())
    st.progress(completed / len(challenge_items))
    st.metric("🌟 Little wins today", f"{completed} / {len(challenge_items)}")
    if completed == len(challenge_items):
        st.balloons()
        st.success("Amazing! 🎉 You checked every item. Remember: this is a fun guide, not a test!")
    elif completed >= 3:
        st.success("You're building some lovely habits! Keep going at your own pace. 💛")
    else:
        st.caption("Every tick is a little win. You can come back and update your checklist!")

else:
    st.markdown('<div class="section-label">Made with care</div>', unsafe_allow_html=True)
    st.title("ℹ️ About MediMate")
    st.markdown("""
    **MediMate** is a colourful student health-education chatbot made with **Python and Streamlit**.

    ### 🌈 What can it do?
    - 💬 Share simple information about common health topics
    - 🌱 Suggest everyday wellness habits
    - 🎯 Help you track a fun daily wellness checklist
    - 🚨 Remind you when to ask a trusted adult for help

    ### 🛟 Important safety note
    MediMate is a learning project. It cannot diagnose illnesses, decide whether a symptom is dangerous, or prescribe medicine. It may misunderstand questions or give incomplete information. Always speak with a trusted adult and a qualified healthcare professional when you are unwell or worried. For an emergency in India, call **112**.
    """)
    st.warning("Please don't enter private details such as your full name, address, school, phone number, or medical records into this demo.", icon="🔐")

st.divider()