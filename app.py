import streamlit as st
import random

# ----- Page Config -----
st.set_page_config(page_title="Dubai Luxury Guessing Game", page_icon="🚗", layout="centered")

# ----- Background Styling + UI -----
page_bg = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1512453979798-5ea266f8880c");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.title {
    font-size: 48px;
    font-weight: bold;
    color: white;
    text-align: center;
    text-shadow: 2px 2px 10px black;
}
.card {
    background-color: rgba(0, 0, 0, 0.65);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-top: 40px;
}
.stButton>button {
    background: linear-gradient(90deg, #FFD700, #FFA500);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    width: 220px;
    border: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    font-size: 18px;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #FFA500, #FFD700);
    color: black;
}

/* Solid color alert bars */
div[data-baseweb="notification"] {
    background-color: #1f3cff !important;
    color: white !important;
    opacity: 1 !important;
    border-radius: 10px !important;
}

/* Success alert */
div[role="alert"][data-testid="stAlertSuccess"] {
    background-color: #00c853 !important;
    color: white !important;
    opacity: 1 !important;
}

/* Error alert */
div[role="alert"][data-testid="stAlertError"] {
    background-color: #d50000 !important;
    color: white !important;
    opacity: 1 !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----- Title -----
st.markdown('<div class="title">🚗 Dubai Luxury Guessing Game</div>', unsafe_allow_html=True)

# ----- Sports Car Prize Pool (stable image links) -----
sports_cars = [
    ("Lamborghini Aventador", "https://upload.wikimedia.org/wikipedia/commons/9/9e/Lamborghini_Aventador_LP700-4.jpg"),
    ("Ferrari 488", "https://upload.wikimedia.org/wikipedia/commons/4/4f/Ferrari_488_GTB_Genf_2015.JPG"),
    ("Bugatti Chiron", "https://upload.wikimedia.org/wikipedia/commons/6/6e/Bugatti_Chiron_IMG_0131.jpg"),
    ("McLaren 720S", "https://upload.wikimedia.org/wikipedia/commons/8/8b/McLaren_720S.jpg"),
    ("Porsche 911 Turbo", "https://upload.wikimedia.org/wikipedia/commons/3/3a/Porsche_911_Turbo_S_%28992%29_IMG_3511.jpg"),
]

# ----- Game State -----
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.game_over = False
    st.session_state.prize = random.choice(sports_cars)

# ----- Game Card -----
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write("I picked a number between 1 and 100.")
st.write(f"You only have {st.session_state.max_attempts} attempts!")

# Typing input
guess = st.number_input("Type your guess:", min_value=1, max_value=100, step=1)

if st.button("Guess Now 🚀") and not st.session_state.game_over:
    st.session_state.attempts += 1

    if guess < st.session_state.secret_number:
        st.warning("Too low! Try higher.")
    elif guess > st.session_state.secret_number:
        st.warning("Too high! Try lower.")
    else:
        st.success("Correct! You won the luxury ride 😎")
        st.balloons()
        car_name, car_img = st.session_state.prize
        st.markdown("---")
        st.subheader(f"🏆 Your Prize: {car_name}")
        st.image(car_img, width=700)
        st.session_state.game_over = True

    if (
        st.session_state.attempts >= st.session_state.max_attempts
        and guess != st.session_state.secret_number
    ):
        st.error("Kaybettin, Dubai bileti kaçtı! ✈️")
        st.write(f"The correct number was: {st.session_state.secret_number}")
        st.session_state.game_over = True

st.write(f"Attempts used: {st.session_state.attempts} / {st.session_state.max_attempts}")

if st.button("Restart Game 🔄"):
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.prize = random.choice(sports_cars)
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
