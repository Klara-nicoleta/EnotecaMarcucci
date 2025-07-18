


import streamlit as st
import json
import random
import os
from datetime import datetime

# Names and tasks
names = ["Klara", "Marco", "Luigi", "Edoardo O", "Edoardo G", "Andrea", "Walter", "Matteo", "Gioel", "Gaia"]
tasks = ["Bicchieri", "Posate", "Pulire Cenci", "Spazzatura Lavaggio", "Gheridon", "Macchina del caffe", "Sistemare cestini del pane"]

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

    num_workers = len(workers)
    num_tasks = len(available_tasks)

    # Calculate how many tasks each worker should get (at least)
    base_tasks_per_worker = num_tasks // num_workers
    extra_tasks = num_tasks % num_workers

    task_index = 0
    for i, worker in enumerate(workers):
        # Determine how many tasks this worker should get
        num_tasks_for_this_worker = base_tasks_per_worker + (1 if i < extra_tasks else 0)
        assigned_tasks = []

        for _ in range(num_tasks_for_this_worker):
            if task_index >= num_tasks:
                break
            assigned_task = available_tasks[task_index]
            # Optional: avoid last assignment from yesterday
            if assigned_task == last_assignments.get(worker):
                # Try to swap if possible
                if task_index + 1 < num_tasks:
                    assigned_task = available_tasks[task_index + 1]
                    available_tasks[task_index + 1] = available_tasks[task_index]
            assigned_tasks.append(assigned_task)
            task_index += 1

        assignments[worker] = assigned_tasks

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
    for worker, worker_tasks in tonight_assignments.items():
        tasks_str = ", ".join(worker_tasks)
        st.write(f"**{worker}** → {tasks_str}")


    st.success("Compiti salvati! Storico aggiornato.")

st.subheader("Storico Assegnazioni")
history = load_history()
if history:
    for entry in reversed(history):
        st.write(f"📅 {entry['date']}")
        for worker, worker_tasks in entry["assignments"].items():
            if isinstance(worker_tasks, list):
                tasks_str = ", ".join(worker_tasks)
            else:
                tasks_str = worker_tasks  # fallback if old data
            st.write(f" - {worker}: {tasks_str}")
else:
    st.write("Nessuno storico ancora.")



