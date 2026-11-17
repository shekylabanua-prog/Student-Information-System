import os, hashlib, secrets
# ----FILE NAMES----
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
        print("Wrong username or Password.")
        pause()
    return None

def add_student():
    header("ADD STUDENT")
    sid = input("Student ID: ").strip()
    if not sid or any(s[0] == sid for s in load(STUDENTS)):
        print("ID is empty or already exists.")
        return pause()
    name = input("Full name: ").strip()
    course = input("Course: ").strip()
    year = input("Year level: ").strip()
    if not year.isdigit():
        print("Year level must be a number.")
        return pause()
    append(STUDENTS, [sid, name, course, year])
    print("Student saved successfully!")
    pause()

def view_students():
    header("ALL STUDENTS")
    table(["ID", "Name", "Course", "Year"], load(STUDENTS))
    pause()

def search_student():
    header("SEARCH STUDENT")
    key = input("Enter ID or name: ").strip().lower()
    found = [s for s in load(STUDENTS) if key in s[0].lower() or key in s[1].lower()]
    table(["ID", "Name", "Course", "Year"], found)
    pause()
    
# Adds a new subject (Admin only)
# Checks: code is not empty or duplicate, title is not empty, units is 1 to 6
def add_subject():
    header("ADD SUBJECT")
    code = input("Subject code: ").strip().upper()
    if not code:
        print("Subject code cannot be empty.")
        return pause()
    if any(s[0] == code for s in load(SUBJECTS)):
        print("Subject code already exists.")
        return pause()
    title = input("Subject title: ").strip()
    if not title:
        print("Subject title cannot be empty.")
        return pause()
    units = input("Units (1-6): ").strip()
    if not units.isdigit() or not 1 <= int(units) <= 6:
        print("Units must be a number from 1 to 6.")
        return pause()
    append(SUBJECTS, [code, title, units])
    print("Subject record saved successfully!")
    pause()

# Shows all saved subjects in a table
def view_subjects():
    header("ALL SUBJECTS")
    table(["Code", "Title", "Units"], load(SUBJECTS))
    pause()

def add_grade():
    header("ADD GRADE")
    sid = input("Student ID:").strip()
    code = input("Subject Code:").strip().upper()
    if not any(s[0] == sid for s in load(STUDENTS)):
        print("Student not found.")
        return pause()
    if not any(s[0] == sid for s in load(STUDENTS)):
        print("Student not found.")
        return pause()
    try:
        g = float(input("Grade(0-100):"))
        if not 0 <= g <= 100:
            raise ValueError
    except ValueError:
        print("Invalid grade.")
        return pause()
    append(GRADES, [sid,code, str(g)])
    print("Grade saved!")
    pause()

def report_card():
    header("STUDENT REPORT CARD")
    sid = input("Student ID: ").strip()
    student = next((s for s in load(STUDENTS) if s[0] == sid), None)
    if not student:
        print("Student not found.")
        return pause()
    titles = {s[0]: s[1] for s in load(SUBJECTS)}
    rows = [[g[1], titles.get(g[1], "?"), g[2]] for g in load(GRADES) if g[0] == sid]
    print(paint(f"\n{student[1]} - {student[2]}"))
    table(["Code", "Subject", "Grade"], rows)
    if rows:
        avg = sum(float(r[2]) for r in rows) / len(rows)
        print(f"Average: {avg:.2f}")
    pause()

def class_summary():
    header("CLASS SUMMARY")
    rows = []
    for sid, name, *_ in load(STUDENTS):
        gs = [float(g[2]) for g in load(GRADES) if g[0] == sid]
        if gs:
            avg = sum(gs) / len(gs)
            rows.append([sid, name, f"{avg:.2f}", "Passed" if avg >= 75 else "Failed"])
    table(["ID", "Name", "Average", "Status"], rows)
    if rows:
        top = max(rows, key=lambda r: float(r[2]))
        print(f"Total students graded: {len(rows)}")
        print(f"Passed: {sum(r[3] == 'Passed' for r in rows)}")
        print(f"Top student: {top[1]} ({top[2]})")
    pause()

def change_theme():
    global color
    header("CHANGE THEME")
    for k, (n, _) in THEMES.items():
        print(f"[{k}] {n}")
    c = input("Choose: ").strip()
    if c in THEMES:
        color = THEMES[c][1]

def change_password(user):
    header("CHANGE PASSWORD")
    new = input("New password: ").strip()
    if len(new) < 6:
        print("At least 6 characters.")
        return pause()
    users = load(USERS)
    for u in users:
        if u[0] == user:
            u[1] = secrets.token_hex(8)
            u[2] = hash_pw(new, u[1])
    save(USERS, users)
    print("Password updated!")
    pause()

def main():
    ensure_admin()
    for f in (STUDENTS, SUBJECTS, GRADES):
        load(f)
    user = login()
    if not user:
        return
    name, role = user
    while True:
        header("MAIN DASHBOARD")
        from datetime import datetime
        print(f"User: {name} ({role})   {datetime.now():%Y-%m-%d %H:%M}\n")
        print("[1] Add Student      [2] View Students")
        print("[3] Search Student   [4] Add Subject (Admin)")
        print("[5] View Subjects    [6] Add Grade")
        print("[7] Report Card      [8] Class Summary")
        print("[9] Change Theme     [10] Change Password")
        print("[0] Logout")
        c = input("\nChoose: ").strip()
        if c == "1": add_student()
        elif c == "2": view_students()
        elif c == "3": search_student()
        elif c == "4":
            if role == "Administrator": add_subject()
            else:
                print("Admins only."); pause()
        elif c == "5": view_subjects()
        elif c == "6": add_grade()
        elif c == "7": report_card()
        elif c == "8": class_summary()
        elif c == "9": change_theme()
        elif c == "10": change_password(name)
        elif c == "0": break
        else:
            print("Invalid choice. Please try again"); pause()

if __name__ == "__main__":
    main()



        