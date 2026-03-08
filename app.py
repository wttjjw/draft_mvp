# pip install streamlit openai pandas

import streamlit as st
from openai import OpenAI
import json
import pandas as pd

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ------------------------------------------------
# LIGHT STYLE
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#f4f6fb;
}

.block-container{
max-width:720px;
margin:auto;
}

.header-card{
background:white;
padding:35px;
border-radius:16px;
box-shadow:0 10px 30px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
}

.place-card{
background:white;
padding:20px;
border-radius:14px;
box-shadow:0 4px 12px rgba(0,0,0,0.07);
margin-bottom:15px;
}

button[kind="primary"]{
background:#6c63ff;
border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# API KEY (SAFE)
# ------------------------------------------------

try:
    api_key = st.secrets["sk-6c4320e4cf78468484e17cc30e018c84"]
except:
    api_key = None

if not api_key:
    st.error("Добавьте DEEPSEEK_API_KEY в secrets или env")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "route" not in st.session_state:
    st.session_state.route = None

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("""
<div class="header-card">
<h1>🌍 AI Travel Planner</h1>
<p>Создайте персональный маршрут путешествия</p>
</div>
""", unsafe_allow_html=True)

st.progress(st.session_state.step/3)

# ------------------------------------------------
# AI GENERATION
# ------------------------------------------------

def generate_route(city, answers):

    prompt = f"""
Создай маршрут по городу {city}.

Предпочтения:
Темп: {answers['pace']}
Интерес: {answers['interest']}
Компания: {answers['company']}

Верни строго JSON:

[
{{"name":"место","desc":"описание","time":60,"lat":59.9,"lon":30.3}},
{{"name":"место","desc":"описание","time":90,"lat":59.9,"lon":30.3}}
]

5 мест.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"user","content":prompt}]
    )

    text = response.choices[0].message.content

    # очистка markdown
    text = text.replace("```json","").replace("```","")

    data = json.loads(text)

    return data

# ------------------------------------------------
# STEP 1
# ------------------------------------------------

if st.session_state.step == 1:

    st.subheader("🏙 Выберите город")

    city = st.text_input(
        "Город",
        placeholder="Например: Санкт-Петербург"
    )

    if st.button("Далее"):

        if city:
            st.session_state.city = city
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Введите город")

# ------------------------------------------------
# STEP 2
# ------------------------------------------------

elif st.session_state.step == 2:

    st.subheader("🧭 Предпочтения")

    pace = st.radio(
        "Темп отдыха",
        ["Активный","Размеренный","Смешанный"]
    )

    interest = st.selectbox(
        "Интерес",
        [
            "История и архитектура",
            "Еда и рестораны",
            "Природа и парки",
            "Музеи",
            "Ночная жизнь"
        ]
    )

    company = st.selectbox(
        "С кем путешествуете",
        ["Один","Вдвоем","С семьей"]
    )

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Назад"):
            st.session_state.step=1
            st.rerun()

    with col2:
        if st.button("Создать маршрут"):

            st.session_state.answers={
                "pace":pace,
                "interest":interest,
                "company":company
            }

            st.session_state.step=3
            st.rerun()

# ------------------------------------------------
# STEP 3
# ------------------------------------------------

elif st.session_state.step == 3:

    st.subheader("🤖 Генерация маршрута")

    if st.session_state.route is None:

        with st.spinner("ИИ анализирует город..."):

            try:

                route = generate_route(
                    st.session_state.city,
                    st.session_state.answers
                )

                st.session_state.route = route

            except Exception as e:

                st.error("Ошибка генерации")
                st.write(e)

    if st.session_state.route:

        st.markdown("## 📍 Маршрут")

        for place in st.session_state.route:

            st.markdown(f"""
            <div class="place-card">
            <h3>📌 {place["name"]}</h3>
            <p>{place["desc"]}</p>
            ⏱ {place["time"]} минут
            </div>
            """, unsafe_allow_html=True)

        # ---------------------------
        # MAP
        # ---------------------------

        try:

            df = pd.DataFrame(st.session_state.route)

            if "lat" in df.columns:

                st.map(df[["lat","lon"]])

        except:
            pass

        if st.button("🔄 Новый маршрут"):

            st.session_state.step = 1
            st.session_state.route = None
            st.rerun()
