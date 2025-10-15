#!/usr/bin/env python3
"""
rail_ticket_app.py
A simple Tkinter ticket booking app using pandas, matplotlib and csv.

Features:
- Search trains (sample static dataset included)
- Book tickets and save to bookings.csv
- View bookings (pandas DataFrame)
- View simple booking statistics chart (matplotlib embedded)

Author: generated for Vishal
"""
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import csv
import os
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------
# Sample train dataset
# ---------------------------
SAMPLE_TRAINS = [
    {"train_no": "12001", "name": "Kolkata Express", "from": "Kolkata", "to": "Delhi", "duration": "22:30"},
    {"train_no": "12951", "name": "Mumbai Rajdhani", "from": "Mumbai", "to": "Delhi", "duration": "17:45"},
    {"train_no": "12863", "name": "Shatabdi AC", "from": "Delhi", "to": "Agra", "duration": "03:20"},
    {"train_no": "11018", "name": "Intercity Fast", "from": "Pune", "to": "Mumbai", "duration": "04:00"},
    {"train_no": "22691", "name": "Duronto Special", "from": "Chennai", "to": "Bengaluru", "duration": "06:30"},
    {"train_no": "15667", "name": "Coastal Queen", "from": "Vijayawada", "to": "Visakhapatnam", "duration": "05:00"},
    {"train_no": "19311", "name": "Humsafar", "from": "Patna", "to": "Howrah", "duration": "12:00"}
]

BOOKINGS_FILE = "bookings.csv"
BOOKING_FIELDS = ["booking_id", "timestamp", "train_no", "train_name", "from", "to", "date", "class", "seats", "passenger_name", "phone", "price_per_seat", "total_price"]

# ---------------------------
# Utilities
# ---------------------------
def ensure_bookings_file():
    """Ensure CSV exists with headers."""
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=BOOKING_FIELDS)
            writer.writeheader()

def read_bookings_df():
    ensure_bookings_file()
    try:
        df = pd.read_csv(BOOKINGS_FILE, parse_dates=["timestamp"])
    except Exception:
        df = pd.DataFrame(columns=BOOKING_FIELDS)
    return df

def append_booking(record: dict):
    ensure_bookings_file()
    with open(BOOKINGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BOOKING_FIELDS)
        writer.writerow(record)

def generate_booking_id():
    return "BK" + datetime.now().strftime("%Y%m%d%H%M%S")

def price_for(train_no, travel_class):
    # Simple price heuristic: base by train_no digits + class multiplier
    base = (sum(int(d) for d in train_no if d.isdigit()) % 500) + 200
    multiplier = {"Sleeper":1.0, "3AC":1.8, "2AC":2.5, "1AC":4.0, "CC":1.3}
    return int(base * multiplier.get(travel_class, 1.0))

# ---------------------------
# Main Application
# ---------------------------
class RailTicketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RailTicket — Simple Ticket Booking App 🚆")
        self.geometry("980x640")
        self.minsize(900, 600)

        # style
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", tabposition='n')
        style.configure("TButton", padding=6)
        style.configure("Accent.TButton", foreground="white", background="#2a9d8f")

        # Notebook tabs
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_search = ttk.Frame(self.nb)
        self.tab_bookings = ttk.Frame(self.nb)
        self.tab_stats = ttk.Frame(self.nb)

        self.nb.add(self.tab_search, text="Search & Book")
        self.nb.add(self.tab_bookings, text="My Bookings")
        self.nb.add(self.tab_stats, text="Stats")

        # Build tabs
        self._build_search_tab()
        self._build_bookings_tab()
        self._build_stats_tab()

        # refresh bookings on start
        self.refresh_bookings_table()
        self.draw_stats_chart()

    # -----------------------
    # Tab: Search & Book
    # -----------------------
    def _build_search_tab(self):
        frame = self.tab_search
        left = ttk.Frame(frame)
        left.pack(side="left", fill="y", padx=12, pady=12)

        right = ttk.Frame(frame)
        right.pack(side="right", fill="both", expand=True, padx=12, pady=12)

        # Search controls
        ttk.Label(left, text="From").pack(anchor="w", pady=(4,0))
        self.ent_from = ttk.Entry(left, width=20)
        self.ent_from.pack(pady=4)

        ttk.Label(left, text="To").pack(anchor="w", pady=(8,0))
        self.ent_to = ttk.Entry(left, width=20)
        self.ent_to.pack(pady=4)

        ttk.Label(left, text="Date (YYYY-MM-DD)").pack(anchor="w", pady=(8,0))
        self.ent_date = ttk.Entry(left, width=20)
        self.ent_date.pack(pady=4)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Button(left, text="Search Trains", command=self.search_trains).pack(pady=(10,4), fill="x")

        # Search results listbox
        ttk.Label(left, text="Available Trains").pack(anchor="w", pady=(10,0))
        self.lst_trains = tk.Listbox(left, height=12, width=40, activestyle='none')
        self.lst_trains.pack(pady=6)
        self.lst_trains.bind("<<ListboxSelect>>", self.on_train_select)

        # Booking form fields on the right
        ttk.Label(right, text="Selected Train", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.lbl_selected = ttk.Label(right, text="(No train selected)", foreground="#555")
        self.lbl_selected.pack(anchor="w", pady=(0,10))

        form = ttk.Frame(right)
        form.pack(anchor="nw", fill="x", pady=6)

        ttk.Label(form, text="Passenger Name").grid(row=0, column=0, sticky="w")
        self.ent_name = ttk.Entry(form, width=34)
        self.ent_name.grid(row=0, column=1, pady=6, padx=6)

        ttk.Label(form, text="Phone").grid(row=1, column=0, sticky="w")
        self.ent_phone = ttk.Entry(form, width=34)
        self.ent_phone.grid(row=1, column=1, pady=6, padx=6)

        ttk.Label(form, text="Class").grid(row=2, column=0, sticky="w")
        self.cmb_class = ttk.Combobox(form, values=["Sleeper", "3AC", "2AC", "1AC", "CC"], state="readonly", width=32)
        self.cmb_class.current(0)
        self.cmb_class.grid(row=2, column=1, pady=6, padx=6)

        ttk.Label(form, text="Seats").grid(row=3, column=0, sticky="w")
        self.spin_seats = ttk.Spinbox(form, from_=1, to=10, width=5)
        self.spin_seats.set(1)
        self.spin_seats.grid(row=3, column=1, sticky="w", pady=6, padx=6)

        ttk.Button(right, text="Book Ticket", command=self.book_ticket, style="Accent.TButton").pack(pady=12, anchor="w")

        # Price preview
        self.lbl_price_preview = ttk.Label(right, text="Price: ₹0  (per seat: ₹0)", font=("Segoe UI", 10))
        self.lbl_price_preview.pack(anchor="w", pady=6)

        # Fill initial train list
        self.display_trains(SAMPLE_TRAINS)

    def display_trains(self, trains):
        self.lst_trains.delete(0, tk.END)
        for t in trains:
            label = f"{t['train_no']} — {t['name']}  [{t['from']} → {t['to']}]  ({t['duration']})"
            self.lst_trains.insert(tk.END, label)
        # store displayed trains reference
        self.current_displayed_trains = trains

    def search_trains(self):
        src = self.ent_from.get().strip()
        dst = self.ent_to.get().strip()
        date_text = self.ent_date.get().strip()
        # validate date format quickly
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Invalid date", "Please enter date in YYYY-MM-DD format.")
            return

        # simple search: filter sample trains by substring matching (case-insensitive)
        results = []
        for t in SAMPLE_TRAINS:
            ok_from = src.lower() in t["from"].lower() if src else True
            ok_to = dst.lower() in t["to"].lower() if dst else True
            if ok_from and ok_to:
                results.append(t)
        if not results:
            messagebox.showinfo("No trains", "No trains found for given route. Try leaving one field empty for broader search.")
        self.display_trains(results)

    def on_train_select(self, event):
        sel = self.lst_trains.curselection()
        if not sel:
            return
        idx = sel[0]
        train = self.current_displayed_trains[idx]
        self.selected_train = train
        self.lbl_selected.config(text=f"{train['train_no']} — {train['name']}  ({train['from']} → {train['to']})")
        # update price preview
        class_choice = self.cmb_class.get()
        seats = int(self.spin_seats.get())
        pps = price_for(train["train_no"], class_choice)
        total = pps * seats
        self.lbl_price_preview.config(text=f"Price: ₹{total}  (per seat: ₹{pps})")

    # -----------------------
    # Booking handling
    # -----------------------
    def book_ticket(self):
        # Must have selected train
        if not hasattr(self, "selected_train") or self.selected_train is None:
            messagebox.showwarning("No train selected", "Please select a train from the list first.")
            return
        name = self.ent_name.get().strip()
        phone = self.ent_phone.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Please enter passenger name.")
            return
        if not phone or not phone.isdigit() or len(phone) < 7:
            messagebox.showwarning("Invalid phone", "Please enter a valid phone number.")
            return
        travel_date = self.ent_date.get().strip()
        try:
            datetime.strptime(travel_date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Invalid date", "Please enter date in YYYY-MM-DD format.")
            return
        seats = int(self.spin_seats.get())
        travel_class = self.cmb_class.get()
        pps = price_for(self.selected_train["train_no"], travel_class)
        total = pps * seats

        # Create booking record
        record = {
            "booking_id": generate_booking_id(),
            "timestamp": datetime.now().isoformat(),
            "train_no": self.selected_train["train_no"],
            "train_name": self.selected_train["name"],
            "from": self.selected_train["from"],
            "to": self.selected_train["to"],
            "date": travel_date,
            "class": travel_class,
            "seats": seats,
            "passenger_name": name,
            "phone": phone,
            "price_per_seat": pps,
            "total_price": total
        }
        append_booking(record)
        messagebox.showinfo("Booked ✔", f"Booking successful!\nBooking ID: {record['booking_id']}\nTotal: ₹{total}")
        # clear some fields
        self.ent_name.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        # refresh bookings tab and stats
        self.refresh_bookings_table()
        self.draw_stats_chart()

    # -----------------------
    # Tab: Bookings table
    # -----------------------
    def _build_bookings_tab(self):
        frame = self.tab_bookings
        top = ttk.Frame(frame)
        top.pack(fill="x", pady=8, padx=8)

        ttk.Button(top, text="Refresh", command=self.refresh_bookings_table).pack(side="left")
        ttk.Button(top, text="Export CSV", command=self.export_bookings).pack(side="left", padx=8)
        ttk.Button(top, text="Delete selected", command=self.delete_selected_booking).pack(side="left")

        # Treeview for bookings
        columns = ("booking_id", "timestamp", "train", "route", "date", "class", "seats", "passenger", "phone", "total")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        heading_map = {
            "booking_id": "Booking ID",
            "timestamp": "Time",
            "train": "Train",
            "route": "Route",
            "date": "Date",
            "class": "Class",
            "seats": "Seats",
            "passenger": "Passenger",
            "phone": "Phone",
            "total": "Total (₹)"
        }
        for col in columns:
            self.tree.heading(col, text=heading_map[col])
            self.tree.column(col, width=100, anchor="center")
        self.tree.column("timestamp", width=140)
        self.tree.column("passenger", width=140)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh_bookings_table(self):
        df = read_bookings_df()
        # clear tree
        for r in self.tree.get_children():
            self.tree.delete(r)
        # insert rows
        if df.empty:
            return
        # sort by time desc
        try:
            df_sorted = df.sort_values("timestamp", ascending=False)
        except Exception:
            df_sorted = df
        for _, row in df_sorted.iterrows():
            tid = row.get("booking_id", "")
            time = str(row.get("timestamp", ""))
            train = f"{row.get('train_no','')} {row.get('train_name','')}"
            route = f"{row.get('from','')}→{row.get('to','')}"
            date = row.get("date", "")
            cls = row.get("class", "")
            seats = int(row.get("seats", 0))
            name = row.get("passenger_name", "")
            phone = row.get("phone", "")
            total = row.get("total_price", 0)
            self.tree.insert("", tk.END, iid=tid, values=(tid, time, train, route, date, cls, seats, name, phone, total))

    def export_bookings(self):
        # Already stored in bookings.csv; just inform user
        if os.path.exists(BOOKINGS_FILE):
            messagebox.showinfo("Exported", f"Bookings already stored in {BOOKINGS_FILE} in current folder.")
        else:
            messagebox.showwarning("No file", "No bookings file found.")

    def delete_selected_booking(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a booking in the table first.")
            return
        bid = sel[0]
        confirm = messagebox.askyesno("Confirm delete", f"Delete booking {bid}? This action cannot be undone.")
        if not confirm:
            return
        # Read CSV, drop booking id, write back
        df = read_bookings_df()
        if "booking_id" in df.columns:
            df2 = df[df["booking_id"] != bid]
            df2.to_csv(BOOKINGS_FILE, index=False)
            messagebox.showinfo("Deleted", f"Booking {bid} removed.")
            self.refresh_bookings_table()
            self.draw_stats_chart()
        else:
            messagebox.showerror("Error", "Could not delete — unexpected CSV format.")

    # -----------------------
    # Tab: Stats (matplotlib)
    # -----------------------
    def _build_stats_tab(self):
        frame = self.tab_stats
        self.stats_frame = ttk.Frame(frame)
        self.stats_frame.pack(fill="both", expand=True, padx=8, pady=8)

        controls = ttk.Frame(self.stats_frame)
        controls.pack(fill="x", pady=(6,12))
        ttk.Label(controls, text="Show bookings grouped by:").pack(side="left")
        self.cmb_stats = ttk.Combobox(controls, values=["train_name", "route", "class", "date"], state="readonly", width=18)
        self.cmb_stats.set("train_name")
        self.cmb_stats.pack(side="left", padx=6)
        ttk.Button(controls, text="Draw", command=self.draw_stats_chart).pack(side="left", padx=6)

        # area for matplotlib canvas
        self.chart_area = ttk.Frame(self.stats_frame)
        self.chart_area.pack(fill="both", expand=True)

    def draw_stats_chart(self):
        # clear chart_area
        for w in self.chart_area.winfo_children():
            w.destroy()
        df = read_bookings_df()
        if df.empty:
            lbl = ttk.Label(self.chart_area, text="No bookings yet — book a ticket to see stats!", foreground="#666")
            lbl.pack(pady=20)
            return
        group_by = self.cmb_stats.get() or "train_name"
        df = df.copy()
        # create route column if needed
        if "route" not in df.columns:
            df["route"] = df.get("from", "") + "→" + df.get("to", "")
        # try group
        try:
            series = df.groupby(group_by)["booking_id"].count().sort_values(ascending=False)
        except Exception:
            # fallback
            series = df["booking_id"].value_counts().head(10)
        # limit to top 8 for clarity
        series = series.head(8)
        labels = list(series.index.astype(str))
        values = list(series.values)

        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title(f"Bookings by {group_by}")
        ax.set_ylabel("Number of bookings")
        ax.set_xlabel(group_by)
        ax.tick_params(axis='x', rotation=30)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)

# ---------------------------
# Run app
# ---------------------------
def main():
    ensure_bookings_file()
    app = RailTicketApp()
    app.mainloop()

if __name__ == "__main__":
    main()
