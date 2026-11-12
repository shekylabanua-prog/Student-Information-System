import os, hashlib, secrets

USERS = "users.txt"
STUDENTS = "students.txt"
SUBJECTS = "subjects.txt"
GRADES = "grades.txt"
RESET = "\033[0m"
THEMES = {"1": ("Green", "\033[92m"), "2": ("Cyan", "\033[96m")}
color = THEMES["1"][1]

def load(path):
    try:
        with open(path, "r") as f:
            return [l.strip().split("|") for l in f if l.strip()]
    except FileNotFoundError:
        open(path, "w").close()
        return []

def save(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write("|".join(r) + "\n")

def append(path, row):
    with open(path, "a") as f:
        f.write("|".join(row) + "\n")