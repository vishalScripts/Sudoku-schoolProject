import tkinter as tk

root = tk.Tk()
root.geometry("1000x600")
root.title("hello")

tk.Label(root, text="Rail Ticket Booking System", font=("Arial", 20)).pack(pady=20)

tk.Button(root, text="Search Trains").pack(pady=10)
tk.Button(root, text="Book Ticket").pack(pady=10)
tk.Button(root, text="View Bookings").pack(pady=10)
tk.Button(root, text="Admin Panel").pack(pady=10)
root.mainloop()
