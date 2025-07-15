import streamlit as st
import json
import random
import os
from datetime import datetime

# Names and tasks
names = ["Klara", "Marco", "Luigi", "Edoardo 1", "Edoardo 2", "Andrea", "Walter", "Matteo"]
tasks = ["Bicchieri", "Bar", "Posate", "Pulire Cenci", "Chiusura Lavaggio", "Gheridon"]

# History
HISTORY_FILE = "assignments.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f: 
            return json.load(f)
    else:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_last_assignments(history):
    if history:
        return history[-1]["assignments"]
    else:
        return {}

def assign_tasks(workers, last_assignments):
    assignments = {}
    available_tasks = tasks.copy()
    random.shuffle(available_tasks)

    for worker in workers:
        last_task = last_assignments.get(worker)
        possible_tasks = [t for t in available_tasks if t != last_task]

        if not possible_tasks:
            assigned_task = available_tasks[0]
        else:
            assigned_task = possible_tasks[0]

        assignments[worker] = assigned_task
        available_tasks.remove(assigned_task)

    return assignments

# Streamlit app
st.title("Assegnazione Turni Ristorante")

st.write("Seleziona chi lavora stasera:")

selected_workers = []
for name in names:
    if st.checkbox(name):
        selected_workers.append(name)

if st.button("Assegna Compiti"):
    history = load_history()
    last_assignments = get_last_assignments(history)
    tonight_assignments = assign_tasks(selected_workers, last_assignments)

    # Save tonight's assignments to history
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assignments": tonight_assignments
    }
    history.append(new_entry)
    save_history(history)

    st.subheader("Compiti per stasera:")
    for worker, task in tonight_assignments.items():
        st.write(f"**{worker}** → {task}")

    st.success("Compiti salvati! Storico aggiornato.")

# Show history
st.subheader("Storico Assegnazioni")
history = load_history()
if history:
    for entry in reversed(history):
        st.write(f"📅 {entry['date']}")
        for worker, task in entry["assignments"].items():
            st.write(f" - {worker}: {task}")
        st.write("---")
else:
    st.write("Nessuno storico ancora.")

