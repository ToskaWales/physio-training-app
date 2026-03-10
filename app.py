import streamlit as st
import json
import os
from datetime import date
import pandas as pd
from exercises import exercises

st.set_page_config(page_title="Physio Training App", layout="wide")

st.title("Physio Training App MVP")

users_file = "users.json"
progress_file = "progress.json"

# Dateien erstellen falls sie nicht existieren
if not os.path.exists(users_file):
    with open(users_file, "w") as f:
        json.dump({}, f)

if not os.path.exists(progress_file):
    with open(progress_file, "w") as f:
        json.dump({}, f)

# Daten laden
with open(users_file) as f:
    users = json.load(f)

with open(progress_file) as f:
    progress = json.load(f)

# Login
st.sidebar.header("Login")

username = st.sidebar.text_input("Username")

if st.sidebar.button("Login"):

    if username not in users:
        users[username] = {"streak": 0}

        with open(users_file, "w") as f:
            json.dump(users, f)

    st.session_state["user"] = username

if "user" not in st.session_state:
    st.warning("Bitte einloggen")
    st.stop()

user = st.session_state["user"]

st.sidebar.success(f"Eingeloggt als {user}")

if user not in progress:
    progress[user] = []

# Trainingsplan
st.header("Dein Trainingsplan")

completed_today = False

for exercise in exercises:

    col1, col2 = st.columns([1,2])

    with col1:
        st.image(exercise["image"], width=200)

    with col2:
        st.subheader(exercise["name"])
        st.write(exercise["description"])
        st.write("Wiederholungen:", exercise["reps"])

        if exercise["name"] in progress[user]:
            st.success("Erledigt")
            completed_today = True
        else:
            if st.button(f"Erledigt: {exercise['name']}"):

                progress[user].append(exercise["name"])

                with open(progress_file, "w") as f:
                    json.dump(progress, f)

                completed_today = True
                st.rerun()

# Fortschritt
st.header("Fortschritt")

total = len(exercises)
done = len(progress[user])

progress_value = done / total

st.progress(progress_value)

st.write(f"{done} von {total} Übungen erledigt")

# Fortschrittsdiagramm
data = pd.DataFrame({
    "Übungen erledigt": [done]
})

st.bar_chart(data)

# Streak
st.header("Trainingsstreak")

today = str(date.today())

if "last_day" not in users[user]:
    users[user]["last_day"] = today

if completed_today and users[user]["last_day"] != today:

    users[user]["streak"] += 1
    users[user]["last_day"] = today

    with open(users_file, "w") as f:
        json.dump(users, f)

st.metric("Aktuelle Streak (Tage)", users[user]["streak"])