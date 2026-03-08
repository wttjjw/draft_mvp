# pip install streamlit requests openai

import streamlit as st
import time
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Travel Guide",
    page_icon="🧭",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #f5f7fa;
}

.main {
    background-color: #f5f7fa;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.place-title {
    font-size: 20px;
    font-weight: 700;
}

.place-desc {
    color: #555;
}

.route-step {
    background: #ffffff;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.step-circle {
    display:inline-block;
    width:30px;
    height:30px;
    border-radius:50%;
    background:#6c63ff;
    color:white;
    text-align:center;
    line-height:30px;
    margin-right:10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "city" not in st.session_state:
    st.session_state.city = None

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "route" not in st.session_state:
    st.session_state.route = None

if "reviews" not in st.session_state:
    st.session_state.reviews = {}

# -----------------------------
# PROGRESS BAR
# -----------------------------
steps = {
    "login": 1,
    "city": 2,
    "quiz": 3,
    "generate": 4,
    "route": 5,
    "reviews": 6
}

current_step = 1

if st.session_state.logged_in:
    current_step = 2
if st.session_state.city:
    current_step = 3
if st.session_state.answers:
    current_step = 4
if st.session_state.route:
    current_step = 5

progress = int((current_step / 6) * 100)

st.progress(progress)

# -----------------------------
# HEADER
# -----------------------------
st.title("🧭 AI Travel Guide")
st.write("Интерактивный помощник для создания идеального маршрута путешествия")

# -----------------------------
# LOGIN
# -----------------------------
if not st.session_state.logged_in:

    st.subheader("Вход")

    name = st.text_input("Введите ваше имя")

    if st.button("Начать"):
        if name:
            st.session_state.user_name = name
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Введите имя")

# -----------------------------
# CITY SELECTION
# -----------------------------
elif not st.session_state.city:

    st.subheader(f"Привет, {st.session_state.user_name} 👋")

    cities = [
        "Москва",
        "Санкт-Петербург",
        "Казань",
        "Сочи",
        "Екатеринбург"
    ]

    city_select = st.selectbox("Выберите город", cities)

    city_input = st.text_input("Или введите свой город")

    if st.button("Продолжить"):

        if city_input:
            st.session_state.city = city_input
        else:
            st.session_state.city = city_select

        st.rerun()

# -----------------------------
# QUIZ
# -----------------------------
elif not st.session_state.answers:

    st.subheader("Небольшой тест")

    pace = st.radio(
        "Какой темп отдыха предпочитаете?",
        ["Активный", "Размеренный", "Смешанный"]
    )

    interest = st.radio(
        "Что вас интересует больше?",
        ["История и архитектура", "Еда и рестораны", "Природа и парки", "Ночная жизнь", "Музеи"]
    )

    company = st.radio(
        "С кем вы путешествуете?",
        ["Один", "Вдвоем", "С семьей"]
    )

    if st.button("Сохранить ответы"):

        st.session_state.answers = {
            "pace": pace,
            "interest": interest,
            "company": company
        }

        st.rerun()

# -----------------------------
# AI GENERATION
# -----------------------------
elif not st.session_state.route:

    st.subheader("Создание маршрута")

    if st.button("Сгенерировать идеальный маршрут"):

        with st.spinner("ИИ анализирует ваши предпочтения..."):
            time.sleep(2)

            st.session_state.route = generate_route(
                st.session_state.city,
                st.session_state.answers
            )

        st.rerun()

# -----------------------------
# SHOW ROUTE
# -----------------------------
else:

    st.subheader(f"Маршрут по городу {st.session_state.city}")

    places = st.session_state.route

    cols = st.columns(2)

    for i, place in enumerate(places):

        with cols[i % 2]:

            st.markdown(f"""
            <div class="card">
            <div class="place-title">📍 {place['name']}</div>
            <div class="place-desc">{place['desc']}</div>
            <br>
            ⏱ Время посещения: {place['time']} минут
            </div>
            """, unsafe_allow_html=True)

            rating = st.slider(
                f"Оценка {place['name']}",
                1,5,
                key=f"rating_{i}"
            )

            review = st.text_input(
                "Ваш отзыв",
                key=f"review_{i}"
            )

            if st.button("Я здесь был", key=f"btn_{i}"):

                st.session_state.reviews[place["name"]] = {
                    "rating": rating,
                    "review": review
                }

                st.success("Отзыв сохранён!")

    st.subheader("Маршрут посещения")

    for i, place in enumerate(places):

        st.markdown(f"""
        <div class="route-step">
        <span class="step-circle">{i+1}</span>
        {place['name']} — примерно {place['time']} мин
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# MOCK AI FUNCTION
# -----------------------------
def generate_route(city, answers):

    """
    Функция имитирует ответ ИИ
    """

    mock_routes = {

        "Москва": [
            {"name": "Красная площадь", "desc": "Главная площадь России", "time": 40},
            {"name": "Кремль", "desc": "Историческая крепость", "time": 120},
            {"name": "Парк Зарядье", "desc": "Современный парк", "time": 60},
            {"name": "Третьяковская галерея", "desc": "Музей искусства", "time": 120},
            {"name": "Арбат", "desc": "Пешеходная улица", "time": 60},
        ],

        "Санкт-Петербург": [
            {"name": "Эрмитаж", "desc": "Один из крупнейших музеев мира", "time": 180},
            {"name": "Дворцовая площадь", "desc": "Историческая площадь", "time": 40},
            {"name": "Невский проспект", "desc": "Главная улица города", "time": 60},
            {"name": "Петропавловская крепость", "desc": "Исторический центр города", "time": 90},
            {"name": "Исаакиевский собор", "desc": "Знаменитый собор", "time": 60},
        ]
    }

    if city in mock_routes:
        return mock_routes[city]

    return random.choice(list(mock_routes.values()))

# -----------------------------
# REAL AI API EXAMPLE
# -----------------------------

"""
Пример подключения OpenAI API

import openai

openai.api_key = "YOUR_API_KEY"

prompt = f'''
Создай туристический маршрут по городу {city}.
Предпочтения пользователя:
{answers}

Верни результат строго в JSON формате:

[
 {{"name":"...", "desc":"...", "time":60}}
]
'''

response = openai.ChatCompletion.create(
 model="gpt-4o-mini",
 messages=[{"role":"user","content":prompt}]
)

json_data = response["choices"][0]["message"]["content"]

return json.loads(json_data)
"""
