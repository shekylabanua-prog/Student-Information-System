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

def paint(t):
    return color + t + RESET
def header(title):
    os.system("cls" if os.name == "nt" else "clear")
    print(paint("=" * 50))
    print(paint(title.center(50)))
    print(paint("=" * 50))

def pause():
    input("\nPress Enter to continue...")

def table(headers, rows):
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    fmt = lambda r: "| " + " | ".join(str(x).ljust(w) for x, w in zip(r, widths)) + " |"
    print(paint(line)); print(fmt(headers)); print(paint(line))
    for r in rows:
        print(fmt(r))
    print(paint(line))
    def hash_pw(pw, salt):
    return hashlib.sha256((salt + pw).encode()).hexdigest()

def ensure_admin():
    if not load(USERS):
        salt = secrets.token_hex(8)
        append(USERS, ["admin", salt, hash_pw("admin123", salt), "Administrator"])
        salt = secrets.token_hex(8)
        append(USERS, ["staff", salt, hash_pw("staff123", salt), "Staff"])

def login():
    for _ in range(3):
        header("STUDENT INFORMATION SYSTEM")
        u = input("Username: ").strip()
        p = input("Password: ").strip()
        for name, salt, h, role in load(USERS):
            if name == u and h == hash_pw(p, salt):
                return name, role
        print("Wrong username or password.")
        pause()
    return None