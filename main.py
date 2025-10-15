#!/usr/bin/env python3
"""
rail_ticket_app_csv.py
Upgraded Tkinter Rail Ticket Booking app backed by CSVs:
 - data/stations.csv
 - data/trains.csv
 - data/schedules.csv
 - data/bookings.csv

Features:
 - Auto-creates sample CSVs if missing
 - Tabs: Dashboard, Book Ticket, Schedules, My Bookings, Stats
 - Modern light UI (ttk) with spacing and clean fonts
 - Use pandas for CSV reads, csv for appends
 - Seat allocation (lowest available seat numbers)
 - Embedded matplotlib chart
Author: generated for Vishal
"""
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import random
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIONS_CSV = os.path.join(DATA_DIR, "stations.csv")
TRAINS_CSV = os.path.join(DATA_DIR, "trains.csv")
SCHEDULES_CSV = os.path.join(DATA_DIR, "schedules.csv")
BOOKINGS_CSV = os.path.join(DATA_DIR, "bookings.csv")

# -----------------------
# Sample CSV contents
# -----------------------
SAMPLE_STATIONS = [
    ("ST001","Mumbai Central","Mumbai"),
    ("ST002","Pune Junction","Pune"),
    ("ST003","Delhi Junction","Delhi"),
    ("ST004","Jaipur Junction","Jaipur"),
    ("ST005","Chennai Central","Chennai"),
    ("ST006","Kolkata Howrah","Kolkata"),
    ("ST007","Ahmedabad Junction","Ahmedabad"),
    ("ST008","Bangalore City","Bangalore"),
    ("ST009","Varanasi Junction","Varanasi"),
    ("ST010","Hyderabad Deccan","Hyderabad"),
]

SAMPLE_TRAINS = [
    ("TR001","Deccan Express","ST001","ST002","200"),
    ("TR002","Rajdhani Express","ST003","ST001","180"),
    ("TR003","Shatabdi Express","ST002","ST003","220"),
    ("TR004","Duronto Express","ST005","ST006","190"),
    ("TR005","Gujarat Mail","ST007","ST001","210"),
    ("TR006","Chennai Superfast","ST005","ST008","240"),
    ("TR007","Kashi Express","ST009","ST003","150"),
    ("TR008","Hyderabad Intercity","ST010","ST005","160"),
    ("TR009","Jaipur Mail","ST004","ST003","170"),
    ("TR010","Bangalore Rajdhani","ST008","ST003","200"),
]

SAMPLE_SCHEDULES = [
    ("SC001","TR001","07:30 AM","11:45 AM","2025-10-16"),
    ("SC002","TR002","08:00 PM","06:15 AM","2025-10-17"),
    ("SC003","TR003","05:00 PM","11:00 PM","2025-10-16"),
    ("SC004","TR004","09:00 AM","08:00 PM","2025-10-17"),
    ("SC005","TR005","06:00 AM","01:30 PM","2025-10-18"),
    ("SC006","TR006","03:30 PM","09:45 PM","2025-10-16"),
    ("SC007","TR007","11:15 AM","08:30 PM","2025-10-17"),
    ("SC008","TR008","07:00 AM","01:15 PM","2025-10-16"),
    ("SC009","TR009","10:30 AM","06:30 PM","2025-10-18"),
    ("SC010","TR010","08:45 PM","05:45 AM","2025-10-17"),
]

SAMPLE_BOOKINGS = [
    ("BK001","Vishal Kumar","TR001","2025-10-16","12","Confirmed"),
    ("BK002","Rahul Mehta","TR002","2025-10-17","34","Confirmed"),
    ("BK003","Ananya Singh","TR003","2025-10-16","89","Pending"),
    ("BK004","Rajesh Patel","TR005","2025-10-18","45","Confirmed"),
    ("BK005","Simran Joshi","TR004","2025-10-17","23","Cancelled"),
    ("BK006","Neha Sharma","TR006","2025-10-16","110","Confirmed"),
    ("BK007","Aditya Rao","TR010","2025-10-17","75","Pending"),
    ("BK008","Ritika Nair","TR007","2025-10-17","61","Confirmed"),
    ("BK009","Deepak Yadav","TR008","2025-10-16","52","Confirmed"),
    ("BK010","Arjun Verma","TR009","2025-10-18","99","Cancelled"),
]

# -----------------------
# Utilities: ensure data dir and files exist
# -----------------------
def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(STATIONS_CSV):
        with open(STATIONS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["station_id","station_name","city"])
            writer.writerows(SAMPLE_STATIONS)

    if not os.path.exists(TRAINS_CSV):
        with open(TRAINS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["train_id","train_name","source_id","destination_id","total_seats"])
            writer.writerows(SAMPLE_TRAINS)

    if not os.path.exists(SCHEDULES_CSV):
        with open(SCHEDULES_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["schedule_id","train_id","departure_time","arrival_time","travel_date"])
            writer.writerows(SAMPLE_SCHEDULES)

    if not os.path.exists(BOOKINGS_CSV):
        with open(BOOKINGS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["booking_id","passenger_name","train_id","travel_date","seat_no","status"])
            writer.writerows(SAMPLE_BOOKINGS)

def read_stations_df():
    return pd.read_csv(STATIONS_CSV, dtype=str)

def read_trains_df():
    return pd.read_csv(TRAINS_CSV, dtype=str)

def read_schedules_df():
    return pd.read_csv(SCHEDULES_CSV, dtype=str)

def read_bookings_df():
    return pd.read_csv(BOOKINGS_CSV, dtype=str)

def append_booking_csv(record: dict):
    # record: booking_id, passenger_name, train_id, travel_date, seat_no, status
    with open(BOOKINGS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([record["booking_id"], record["passenger_name"], record["train_id"],
                         record["travel_date"], record["seat_no"], record["status"]])

def gen_booking_id():
    return "BK" + datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(10,99))

# -----------------------
# Seat allocation helper
# -----------------------
def available_seats_for(train_id, travel_date, total_seats):
    """
    Compute lowest available seat numbers for train_id on travel_date.
    Returns a sorted list of available seat integers.
    """
    dfb = read_bookings_df()
    # select confirmed and pending seats for that train/date
    taken = set()
    if not dfb.empty:
        dfb = dfb.fillna("")
        sel = dfb[(dfb["train_id"] == train_id) & (dfb["travel_date"] == travel_date)]
        for val in sel["seat_no"].astype(str).tolist():
            try:
                taken.add(int(val))
            except Exception:
                pass
    all_seats = set(range(1, int(total_seats)+1))
    avail = sorted(list(all_seats - taken))
    return avail

# -----------------------
# UI: Main Application
# -----------------------
class RailApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RailTicket — CSV Powered (Light Modern UI) 🚆")
        self.geometry("1050x650")
        self.minsize(980, 600)

        # style
        self.setup_style()

        # Notebook (tabs)
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=12, pady=12)

        # tabs
        self.tab_dashboard = ttk.Frame(self.nb)
        self.tab_book = ttk.Frame(self.nb)
        self.tab_schedules = ttk.Frame(self.nb)
        self.tab_bookings = ttk.Frame(self.nb)
        self.tab_stats = ttk.Frame(self.nb)

        self.nb.add(self.tab_dashboard, text="Dashboard")
        self.nb.add(self.tab_book, text="Book Ticket")
        self.nb.add(self.tab_schedules, text="Schedules")
        self.nb.add(self.tab_bookings, text="My Bookings")
        self.nb.add(self.tab_stats, text="Stats")

        # Build UIs
        self.build_dashboard()
        self.build_book_tab()
        self.build_schedules_tab()
        self.build_bookings_tab()
        self.build_stats_tab()

        # initial loads
        self.load_station_train_data()
        self.refresh_schedules_tree()
        self.refresh_bookings_table()
        self.draw_stats()

    def setup_style(self):
        style = ttk.Style(self)
        # use clam or default
        try:
            style.theme_use("clam")
        except Exception:
            pass
        # colors for light modern look
        primary = "#2b7a78"   # teal-ish
        accent = "#83c5be"
        bg = "#f7fbfb"
        card = "#ffffff"

        self.configure(bg=bg)
        style.configure("TFrame", background=bg)
        style.configure("Card.TFrame", background=card, relief="flat")
        style.configure("TLabel", background=bg, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background=bg)
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("Accent.TButton", background=primary, foreground="white")
        style.map("Accent.TButton", background=[('active', accent)])

        # Treeview style
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[('selected', primary)])

    # -----------------------
    # Dashboard Tab
    # -----------------------
    def build_dashboard(self):
        f = ttk.Frame(self.tab_dashboard, padding=12)
        f.pack(fill="both", expand=True)

        # ---- Title ----
        header = ttk.Label(f, text="Welcome to RailTicket", style="Header.TLabel")
        header.pack(anchor="w")

        subtitle = ttk.Label(
            f,
            text="Light modern UI • CSV-backed • Tabs for workflow",
            foreground="#666"
        )
        subtitle.pack(anchor="w", pady=(2, 12))

        # ---- Hero / Dashboard Image ----
        hero_frame = tk.Frame(f, bg="#dfe6e9", height=300)  # adjustable height
        hero_frame.pack(fill="x", pady=(0, 20))
        hero_frame.pack_propagate(False)

        # image inside the hero
        canvas = tk.Canvas(hero_frame, width=900, height=300, highlightthickness=0)
        canvas.pack(fill="x")
        self.dashboard_img = tk.PhotoImage(file="dashboard.png").subsample(4,4)
        canvas.create_image(600, 130, image=self.dashboard_img)



        # ---- Stat cards overlay ----
        cards_frame = tk.Frame(hero_frame, bg="", height=120)
        cards_frame.place(x=300, rely=1.0, anchor="s", y=-10)  # floats near bottom

        # individual cards
        self.card_total_trains = self.make_stat_card(cards_frame, "Trains", "—")
        self.card_total_stations = self.make_stat_card(cards_frame, "Stations", "—")
        self.card_next_schedule = self.make_stat_card(cards_frame, "Next Schedule", "—")

        # ---- Right side button below image ----
        action_frame = tk.Frame(hero_frame, bg="", height=120)
        action_frame.place(relx=0.9, rely=1.0, anchor="s", y=-10, x=35)
        ttk.Button(action_frame, text="Refresh Data", command=self.refresh_all_data, style="Accent.TButton").pack(anchor="e")

        # ---- Help / Tips Section ----
        help_box = ttk.LabelFrame(f, text="Quick tips", padding=10, style="Card.TFrame")
        help_box.pack(fill="both", expand=True, pady=12)
        txt = (
            "• Use the 'Book Ticket' tab to search trains by station or schedule.\n"
            "• 'Schedules' lists upcoming runs and lets you pick a date.\n"
            "• Bookings are saved to data/bookings.csv — you can view/delete them in 'My Bookings'.\n"
            "• Stats show bookings grouped by train or date."
        )
        lbl = ttk.Label(help_box, text=txt, wraplength=880, foreground="#333")
        lbl.pack(anchor="w")


    def make_stat_card(self, parent, title, value):
        # ---- Simulated rounded cards using padding and background ----
        card = tk.Frame(parent, bg="#ffffff", highlightbackground="#ccc", highlightthickness=1)
        card.pack(side="left", padx=0, ipadx=0, ipady=0)

        ttk.Label(card, text=title, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        v = ttk.Label(card, text=value, font=("Segoe UI", 20, "bold"))
        v.pack(anchor="w", pady=(0, 0), padx=10)
        return v


    def refresh_all_data(self):
        self.load_station_train_data()
        self.refresh_schedules_tree()
        self.refresh_bookings_table()
        self.draw_stats()
        messagebox.showinfo("Refreshed", "Data refreshed from CSV files.")

    # -----------------------
    # Load station/train data
    # -----------------------
    def load_station_train_data(self):
        self.stations = read_stations_df()
        self.trains = read_trains_df()
        self.schedules = read_schedules_df()
        # update stat cards
        self.card_total_trains.config(text=str(len(self.trains)))
        self.card_total_stations.config(text=str(len(self.stations)))
        # compute next schedule (earliest upcoming travel_date >= today)
        try:
            today = datetime.now().date()
            df = self.schedules.copy()
            df['dt'] = pd.to_datetime(df['travel_date'], errors='coerce').dt.date
            upcoming = df[df['dt'] >= today].sort_values('dt')
            if not upcoming.empty:
                r = upcoming.iloc[0]
                train_name = self.trains[self.trains['train_id'] == r['train_id']]['train_name'].values[0]
                self.card_next_schedule.config(text=f"{train_name} on {r['travel_date']}")
            else:
                self.card_next_schedule.config(text="No upcoming schedules")
        except Exception:
            self.card_next_schedule.config(text="—")

    # -----------------------
    # Book Ticket Tab
    # -----------------------
    def build_book_tab(self):
        f = ttk.Frame(self.tab_book, padding=12)
        f.pack(fill="both", expand=True)

        left = ttk.Frame(f)
        left.pack(side="left", fill="y", padx=(0,12))

        ttk.Label(left, text="Search by Station", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Label(left, text="From station (partial)").pack(anchor="w", pady=(6,0))
        self.ent_from = ttk.Entry(left, width=28)
        self.ent_from.pack(pady=6)

        ttk.Label(left, text="To station (partial)").pack(anchor="w")
        self.ent_to = ttk.Entry(left, width=28)
        self.ent_to.pack(pady=6)

        ttk.Label(left, text="Travel date (YYYY-MM-DD)").pack(anchor="w")
        self.ent_date = ttk.Entry(left, width=28)
        self.ent_date.pack(pady=6)

        ttk.Button(left, text="Search Trains", command=self.search_trains_for_booking, style="Accent.TButton").pack(pady=(10,6), fill="x")

        ttk.Separator(f, orient="vertical").pack(side="left", fill="y", padx=12)

        right = ttk.Frame(f)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Search results", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.search_tree = ttk.Treeview(right, columns=("train_id","train_name","route","seats"), show="headings", height=8)
        self.search_tree.heading("train_id", text="Train ID")
        self.search_tree.heading("train_name", text="Train")
        self.search_tree.heading("route", text="Route")
        self.search_tree.heading("seats", text="Seats")
        self.search_tree.pack(fill="x", pady=6)
        self.search_tree.bind("<<TreeviewSelect>>", self.on_search_select)

        # booking form
        form = ttk.LabelFrame(right, text="Book selected train", padding=10, style="Card.TFrame")
        form.pack(fill="both", expand=True, pady=8)
        ttk.Label(form, text="Passenger name").grid(row=0, column=0, sticky="w")
        self.book_name = ttk.Entry(form, width=36)
        self.book_name.grid(row=0, column=1, pady=6, padx=6)

        ttk.Label(form, text="Phone").grid(row=1, column=0, sticky="w")
        self.book_phone = ttk.Entry(form, width=36)
        self.book_phone.grid(row=1, column=1, pady=6, padx=6)

        ttk.Label(form, text="Seats to book").grid(row=2, column=0, sticky="w")
        self.spin_seats = ttk.Spinbox(form, from_=1, to=6, width=6)
        self.spin_seats.set(1)
        self.spin_seats.grid(row=2, column=1, sticky="w", pady=6, padx=6)

        ttk.Label(form, text="Selected schedule").grid(row=3, column=0, sticky="w")
        self.sel_schedule_lbl = ttk.Label(form, text="(none)")
        self.sel_schedule_lbl.grid(row=3, column=1, sticky="w", pady=6, padx=6)

        ttk.Button(form, text="Show available seats", command=self.show_available_seats).grid(row=4, column=0, pady=8)
        ttk.Button(form, text="Book Now", command=self.book_now, style="Accent.TButton").grid(row=4, column=1, pady=8, sticky="w")

        self.available_seats_box = ScrolledText(form, height=4, width=48)
        self.available_seats_box.grid(row=5, column=0, columnspan=2, pady=(6,0))

        # internal selection
        self.selected_schedule = None

    def search_trains_for_booking(self):
        src = self.ent_from.get().strip().lower()
        dst = self.ent_to.get().strip().lower()
        date = self.ent_date.get().strip()
        # validate date loosely
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Invalid date", "Please use YYYY-MM-DD format.")
            return
        # find station ids matching input
        st_df = self.stations.fillna("")
        matched_from = st_df[st_df['station_name'].str.lower().str.contains(src)] if src else st_df
        matched_to = st_df[st_df['station_name'].str.lower().str.contains(dst)] if dst else st_df

        # find trains where source in matched_from and dest in matched_to
        tr_df = self.trains.fillna("")
        results = []
        for _, tr in tr_df.iterrows():
            if (tr['source_id'] in matched_from['station_id'].values) and (tr['destination_id'] in matched_to['station_id'].values):
                results.append(tr)

        # Also consider schedules on that date for trains
        sched_df = self.schedules.fillna("")
        sched_on_date = sched_df[sched_df['travel_date'] == date]
        # Filter results to ones that have schedule on that date
        sched_trains = set(sched_on_date['train_id'].values.tolist())
        filtered = [r for r in results if r['train_id'] in sched_trains]

        # show in tree
        for r in self.search_tree.get_children():
            self.search_tree.delete(r)
        if not filtered:
            messagebox.showinfo("No trains", "No trains found for that route and date.")
            return
        for tr in filtered:
            src_name = self.stations[self.stations['station_id'] == tr['source_id']]['station_name'].values[0]
            dst_name = self.stations[self.stations['station_id'] == tr['destination_id']]['station_name'].values[0]
            # seats field is total seats
            self.search_tree.insert("", tk.END, iid=tr['train_id'], values=(tr['train_id'], tr['train_name'], f"{src_name}→{dst_name}", tr['total_seats']))

    def on_search_select(self, event):
        sel = self.search_tree.selection()
        if not sel:
            return
        tid = sel[0]
        # find schedule options for this train & selected date
        date = self.ent_date.get().strip()
        sf = self.schedules[(self.schedules['train_id'] == tid) & (self.schedules['travel_date'] == date)]
        if sf.empty:
            self.selected_schedule = None
            self.sel_schedule_lbl.config(text="No schedule on this date")
            self.available_seats_box.delete("1.0", tk.END)
        else:
            # if multiple schedules, pick first (or allow choose later)
            row = sf.iloc[0]
            sched_text = f"{row['schedule_id']} — {row['departure_time']} → {row['arrival_time']} on {row['travel_date']}"
            self.sel_schedule_lbl.config(text=sched_text)
            self.selected_schedule = row.to_dict()
            # update available seats box
            self.show_available_seats()

    def show_available_seats(self):
        if not self.selected_schedule:
            messagebox.showwarning("No schedule", "Select a train and schedule first.")
            return
        train_id = self.selected_schedule['train_id']
        travel_date = self.selected_schedule['travel_date']
        total_seats = int(self.trains[self.trains['train_id'] == train_id]['total_seats'].values[0])
        avail = available_seats_for(train_id, travel_date, total_seats)
        if not avail:
            self.available_seats_box.delete("1.0", tk.END)
            self.available_seats_box.insert("1.0", "No seats available.")
            return
        # show first 40 available seats nicely
        display = ", ".join(str(x) for x in avail[:80])
        self.available_seats_box.delete("1.0", tk.END)
        self.available_seats_box.insert("1.0", f"Available seats (first shown):\n{display}")

    def book_now(self):
        name = self.book_name.get().strip()
        phone = self.book_phone.get().strip()
        try:
            seats_needed = int(self.spin_seats.get())
        except Exception:
            messagebox.showerror("Invalid seats", "Enter a valid number of seats.")
            return
        if not name:
            messagebox.showwarning("Missing name", "Enter passenger name.")
            return
        if not phone or not phone.isdigit() or len(phone) < 7:
            messagebox.showwarning("Invalid phone", "Enter a valid phone number.")
            return
        if not self.selected_schedule:
            messagebox.showwarning("No schedule", "Select a train & schedule first.")
            return
        train_id = self.selected_schedule['train_id']
        travel_date = self.selected_schedule['travel_date']
        total_seats = int(self.trains[self.trains['train_id'] == train_id]['total_seats'].values[0])
        avail = available_seats_for(train_id, travel_date, total_seats)
        if len(avail) < seats_needed:
            messagebox.showerror("Not enough seats", f"Only {len(avail)} seats available.")
            return
        # allocate lowest seat numbers
        allocated = avail[:seats_needed]
        # append bookings for each seat
        for s in allocated:
            rec = {
                "booking_id": gen_booking_id(),
                "passenger_name": name,
                "train_id": train_id,
                "travel_date": travel_date,
                "seat_no": str(s),
                "status": "Confirmed"
            }
            append_booking_csv(rec)
        messagebox.showinfo("Booked", f"Booked seats: {', '.join(str(x) for x in allocated)}\nBooking saved to data/bookings.csv")
        # refresh
        self.refresh_bookings_table()
        self.show_available_seats()
        self.draw_stats()

    # -----------------------
    # Schedules Tab
    # -----------------------
    def build_schedules_tab(self):
        f = ttk.Frame(self.tab_schedules, padding=12)
        f.pack(fill="both", expand=True)
        top = ttk.Frame(f)
        top.pack(fill="x")

        ttk.Label(top, text="Upcoming Schedules", style="Header.TLabel").pack(anchor="w")
        self.sched_tree = ttk.Treeview(f, columns=("schedule_id","train","route","dep","arr","date"), show="headings", height=12)
        self.sched_tree.heading("schedule_id", text="Schedule ID")
        self.sched_tree.heading("train", text="Train")
        self.sched_tree.heading("route", text="Route")
        self.sched_tree.heading("dep", text="Dep")
        self.sched_tree.heading("arr", text="Arr")
        self.sched_tree.heading("date", text="Date")
        self.sched_tree.pack(fill="both", expand=True, pady=8)
        self.sched_tree.bind("<Double-1>", self.on_schedule_double)

    def refresh_schedules_tree(self):
        for r in self.sched_tree.get_children():
            self.sched_tree.delete(r)
        df = self.schedules.fillna("")
        for _, row in df.iterrows():
            train_name = self.trains[self.trains['train_id'] == row['train_id']]['train_name'].values[0]
            tr = self.trains[self.trains['train_id'] == row['train_id']].iloc[0]
            src_name = self.stations[self.stations['station_id'] == tr['source_id']]['station_name'].values[0]
            dst_name = self.stations[self.stations['station_id'] == tr['destination_id']]['station_name'].values[0]
            self.sched_tree.insert("", tk.END, iid=row['schedule_id'], values=(row['schedule_id'], train_name, f"{src_name}→{dst_name}", row['departure_time'], row['arrival_time'], row['travel_date']))

    def on_schedule_double(self, event):
        sel = self.sched_tree.selection()
        if not sel:
            return
        sid = sel[0]
        row = self.schedules[self.schedules['schedule_id'] == sid].iloc[0]
        # jump to Book Ticket tab and prefill
        self.nb.select(self.tab_book)
        # set from/to based on train
        tr = self.trains[self.trains['train_id'] == row['train_id']].iloc[0]
        src_name = self.stations[self.stations['station_id'] == tr['source_id']]['station_name'].values[0]
        dst_name = self.stations[self.stations['station_id'] == tr['destination_id']]['station_name'].values[0]
        self.ent_from.delete(0, tk.END); self.ent_from.insert(0, src_name)
        self.ent_to.delete(0, tk.END); self.ent_to.insert(0, dst_name)
        self.ent_date.delete(0, tk.END); self.ent_date.insert(0, row['travel_date'])
        # run search and select the train
        self.search_trains_for_booking()
        # select tree item for this train
        try:
            self.search_tree.selection_set(tr['train_id'])
            self.on_search_select(None)
        except Exception:
            pass

    # -----------------------
    # My Bookings Tab
    # -----------------------
    def build_bookings_tab(self):
        f = ttk.Frame(self.tab_bookings, padding=12)
        f.pack(fill="both", expand=True)
        top = ttk.Frame(f)
        top.pack(fill="x")
        ttk.Button(top, text="Refresh", command=self.refresh_bookings_table).pack(side="left")
        ttk.Button(top, text="Export CSV (data/bookings.csv)", command=lambda: messagebox.showinfo("Path", f"Bookings file: {BOOKINGS_CSV}")).pack(side="left", padx=6)
        ttk.Button(top, text="Delete Selected", command=self.delete_selected_booking).pack(side="left", padx=6)

        cols = ("booking_id","passenger","train","date","seat","status")
        self.bookings_tree = ttk.Treeview(f, columns=cols, show="headings", height=18)
        for c in cols:
            self.bookings_tree.heading(c, text=c.replace("_"," ").title())
        self.bookings_tree.pack(fill="both", expand=True, pady=8)

    def refresh_bookings_table(self):
        for r in self.bookings_tree.get_children():
            self.bookings_tree.delete(r)
        df = read_bookings_df().fillna("")
        if df.empty:
            return
        # sort by booking_id (time encoded) descending
        try:
            df_sorted = df.sort_values("booking_id", ascending=False)
        except Exception:
            df_sorted = df
        for _, row in df_sorted.iterrows():
            train_name = self.trains[self.trains['train_id'] == row['train_id']]['train_name'].values[0] if row['train_id'] in self.trains['train_id'].values else row['train_id']
            self.bookings_tree.insert("", tk.END, iid=row['booking_id'], values=(row['booking_id'], row['passenger_name'], train_name, row['travel_date'], row['seat_no'], row['status']))

    def delete_selected_booking(self):
        sel = self.bookings_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a booking to delete.")
            return
        bid = sel[0]
        ok = messagebox.askyesno("Confirm", f"Delete booking {bid}?")
        if not ok:
            return
        df = read_bookings_df()
        df2 = df[df['booking_id'] != bid]
        df2.to_csv(BOOKINGS_CSV, index=False)
        self.refresh_bookings_table()
        self.draw_stats()
        messagebox.showinfo("Deleted", f"Booking {bid} removed.")

    # -----------------------
    # Stats Tab
    # -----------------------
    def build_stats_tab(self):
        f = ttk.Frame(self.tab_stats, padding=12)
        f.pack(fill="both", expand=True)
        top = ttk.Frame(f)
        top.pack(fill="x")
        ttk.Label(top, text="Booking Statistics", style="Header.TLabel").pack(side="left")
        self.cmb_stats = ttk.Combobox(top, values=["train_id","travel_date","status"], state="readonly", width=18)
        self.cmb_stats.set("train_id")
        self.cmb_stats.pack(side="left", padx=6)
        ttk.Button(top, text="Draw", command=self.draw_stats).pack(side="left")

        self.chart_area = ttk.Frame(f)
        self.chart_area.pack(fill="both", expand=True, pady=8)

    def draw_stats(self):
        for w in self.chart_area.winfo_children():
            w.destroy()
        df = read_bookings_df()
        if df.empty:
            ttk.Label(self.chart_area, text="No bookings yet", foreground="#666").pack(pady=20)
            return
        group_by = self.cmb_stats.get() or "train_id"
        try:
            series = df.groupby(group_by)["booking_id"].count().sort_values(ascending=False)
        except Exception:
            series = df['booking_id'].value_counts().head(8)
        series = series.head(8)
        labels = list(series.index.astype(str))
        values = list(series.values)

        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title(f"Bookings by {group_by}")
        ax.set_ylabel("Count")
        ax.set_xlabel(group_by)
        ax.tick_params(axis='x', rotation=30)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# -----------------------
# Run
# -----------------------
def main():
    ensure_data_files()
    app = RailApp()
    app.mainloop()

if __name__ == "__main__":
    main()
