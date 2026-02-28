import streamlit as st
import random
import sqlite3

# ----- DATABASE SETUP -----
conn = sqlite3.connect("scores.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS scores (
    username TEXT,
    attempts INTEGER
)
""")
conn.commit()

# ----- FUNCTIONS -----
def save_score(username, attempts):
    # Check if user already has a record
    c.execute("SELECT attempts FROM scores WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        best_attempts = result[0]
        if attempts < best_attempts:
            c.execute("UPDATE scores SET attempts = ? WHERE username = ?", (attempts, username))
    else:
        c.execute("INSERT INTO scores (username, attempts) VALUES (?, ?)", (username, attempts))

    conn.commit()

def get_leaderboard():
    c.execute("SELECT username, attempts FROM scores ORDER BY attempts ASC LIMIT 5")
    return c.fetchall()

def get_user_best(username):
    c.execute("SELECT attempts FROM scores WHERE username = ?", (username,))
    return c.fetchone()

# ----- PAGE CONFIG -----
st.set_page_config(page_title="Dubai Luxury Guessing Game", page_icon="🚗", layout="centered")

# ----- TITLE -----
st.title("🚗 Dubai Luxury Guessing Game")

# ----- USERNAME INPUT -----
username = st.text_input("Enter your name to track your personal record:")

# ----- GAME STATE -----
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.game_over = False

# ----- GAME UI -----
st.write("Guess the secret number between 1 and 100.")
st.write(f"You have {st.session_state.max_attempts} attempts.")

guess_input = st.text_input("Type your guess (1-100):")

guess = None
if guess_input.isdigit():
    guess = int(guess_input)

if st.button("Guess Now 🚀") and not st.session_state.game_over and username:
    st.session_state.attempts += 1

    if guess < st.session_state.secret_number:
        st.warning("Your guess is too low. Try a higher number.")
    elif guess > st.session_state.secret_number:
        st.warning("Your guess is too high. Try a lower number.")
    else:
        st.success("Correct! You won the luxury ride 😎")
        st.balloons()

        save_score(username, st.session_state.attempts)
        st.session_state.game_over = True

    if (
        st.session_state.attempts >= st.session_state.max_attempts
        and guess != st.session_state.secret_number
    ):
        st.error("You lost! The Dubai ticket slipped away ✈️")
        st.write(f"The correct number was: {st.session_state.secret_number}")
        st.session_state.game_over = True

st.write(f"Attempts used: {st.session_state.attempts} / {st.session_state.max_attempts}")

# ----- PERSONAL RECORD -----
if username:
    best = get_user_best(username)
    if best:
        st.info(f"🏆 Your Best Record: {best[0]} attempts")

# ----- GLOBAL LEADERBOARD -----
st.subheader("🌍 Global Leaderboard (Top 5)")
leaderboard = get_leaderboard()

if leaderboard:
    for i, (user, score) in enumerate(leaderboard, start=1):
        st.write(f"{i}. {user} — {score} attempts")
else:
    st.write("No scores yet. Be the first champion!")

# ----- RESTART BUTTON -----
if st.button("Restart Game 🔄"):
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.rerun()

