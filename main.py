import pandas as pd  # For handling CSV data as DataFrames
import csv           # For writing bookings to CSV
import matplotlib.pyplot as plt  # (Unused) For plotting, if needed

# File paths for train and booking data
TRAINS_FILE = './data/trains.csv'
BOOKINGS_FILE = './data/bookings.csv'

def load_trains():
    """
    Loads train data from the CSV file into a pandas DataFrame.
    """
    return pd.read_csv(TRAINS_FILE)

def show_trains(trains):
    """
    Displays a list of available trains with their details.
    """
    print("\n=== Available Trains ===")
    # Show selected columns without DataFrame index
    print(trains[['train_no', 'train_name', 'from_station', 'to_station']].to_string(index=False))

def book_ticket(trains):
    """
    Books a ticket for a user:
    - Prompts for train number, passenger name, age, and seats.
    - Checks for valid train and seat availability.
    - Updates seats in the trains DataFrame and CSV.
    - Appends booking info to the bookings CSV.
    """
    train_no = input("Enter train number to book: ")
    # Check if train number exists
    if train_no not in trains['train_no'].astype(str).values:
        print("❌ Invalid train number.")
        return

    name = input("Enter passenger name: ")
    age = input("Enter age: ")
    seats = int(input("Enter number of seats to book: "))

    # Get the selected train row
    train = trains[trains['train_no'].astype(str) == train_no].iloc[0]
    remaining_seats = train['total_seats']

    # Check seat availability
    if seats > remaining_seats:
        print("❌ Not enough seats available.")
        return

    # Update seat count in DataFrame and save to CSV
    trains.loc[trains['train_no'] == int(train_no), 'total_seats'] -= seats
    trains.to_csv(TRAINS_FILE, index=False)

    # Save booking to bookings CSV
    with open(BOOKINGS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, age, train_no, seats])

    print(f"✅ Ticket booked successfully for {name} on {train['train_name']}!")

def show_bookings():
    """
    Displays all bookings from the bookings CSV file.
    """
    try:
        df = pd.read_csv(BOOKINGS_FILE)
        print("\n=== All Bookings ===")
        print(df.to_string(index=False))
    except FileNotFoundError:
        print("No bookings yet.")

def main():
    """
    Main loop for the ticket booking system.
    Presents a menu and calls the appropriate functions.
    """
    trains = load_trains()
    while True:
        print("\n===== RAIL TICKET SYSTEM =====")
        print("1. Show Trains")
        print("2. Book Ticket")
        print("3. View Bookings")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            show_trains(trains)
        elif choice == '2':
            book_ticket(trains)
        elif choice == '3':
            show_bookings()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
