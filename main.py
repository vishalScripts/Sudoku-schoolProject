import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Rail Ticket Booking System")
root.geometry("900x600")
root.config(bg="#e9e4db")  # light beige background

# ====== TITLE BAR ======
title = tk.Label(
    root,
    text="🚆 Indian Rail Ticket Booking",
    font=("Poppins", 20, "bold"),
    bg="#2f5d8a",
    fg="white",
    pady=15
)
title.pack(fill="x")

# ====== MAIN FRAME ======
main_frame = tk.Frame(root, bg="#e9e4db")
main_frame.pack(pady=30)

# ==== LEFT PANEL - Inputs ====
left_frame = tk.Frame(main_frame, bg="#e9e4db")
left_frame.pack(side="left", padx=40)

tk.Label(left_frame, text="From Station", font=("Poppins", 12), bg="#e9e4db").pack(anchor="w")
from_box = ttk.Combobox(left_frame, values=["Delhi", "Mumbai", "Kolkata", "Chennai", "Jaipur"], width=25)
from_box.pack(pady=5)

tk.Label(left_frame, text="To Station", font=("Poppins", 12), bg="#e9e4db").pack(anchor="w", pady=(10,0))
to_box = ttk.Combobox(left_frame, values=["Delhi", "Mumbai", "Kolkata", "Chennai", "Jaipur"], width=25)
to_box.pack(pady=5)

tk.Label(left_frame, text="Date of Journey", font=("Poppins", 12), bg="#e9e4db").pack(anchor="w", pady=(10,0))
date_entry = ttk.Entry(left_frame, width=27)
date_entry.pack(pady=5)

tk.Label(left_frame, text="Class", font=("Poppins", 12), bg="#e9e4db").pack(anchor="w", pady=(10,0))
class_box = ttk.Combobox(left_frame, values=["Sleeper", "3A", "2A", "1A", "General"], width=25)
class_box.pack(pady=5)

# ====== BUTTON ======
book_btn = tk.Button(
    left_frame,
    text="Search Trains",
    bg="#2f5d8a",
    fg="white",
    font=("Poppins", 12, "bold"),
    width=20,
    height=1,
    relief="flat",
    cursor="hand2"
)
book_btn.pack(pady=20)

# ====== RIGHT PANEL - Train Display ======
right_frame = tk.Frame(main_frame, bg="#e9e4db")
right_frame.pack(side="right", padx=40)

canvas = tk.Canvas(right_frame, width=500, height=300, bg="#b9d3dc", highlightthickness=0)
canvas.pack()

# Platform
canvas.create_rectangle(0, 260, 500, 300, fill="#555555", outline="")

# Train Body
x, y = 50, 200
colors = ["#2f5d8a", "#c8473b", "#efe6ca", "#a8b866", "#e0c150"]
labels = ["LOCO", "COACH", "SLEEPER", "AC", "GENERAL"]

for i in range(5):
    canvas.create_rectangle(x, y, x+80, y+50, fill=colors[i], outline="black")
    canvas.create_text(x+40, y+25, text=labels[i], fill="white" if i < 2 else "black", font=("Poppins", 8, "bold"))
    canvas.create_oval(x+10, y+45, x+25, y+60, fill="black")
    canvas.create_oval(x+55, y+45, x+70, y+60, fill="black")
    x += 90

# ====== FOOTER ======
footer = tk.Label(
    root,
    text="© 2025 Indian Rail Systems | Designed by Vishal",
    font=("Poppins", 9),
    bg="#2f5d8a",
    fg="white",
    pady=10
)
footer.pack(side="bottom", fill="x")

root.mainloop()
