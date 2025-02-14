# Handles menu system for flight management
# Maps menu items to functions

import tabulate
from db_operations import DBOperations

def display_menu():
    """Displays the main menu options."""
    options = [
        "1. Create Tables",
        "2. Insert Flight",
        "3. View All Flights",
        "4. Search Flights",
        "5. Update Flight Info",
        "6. Delete Flight",
        "7. Assign Pilot",
        "8. View Flight Count Per Destination",
        "9. View Flight Count Per Pilot",
        "10. Exit"
    ]
    print("\n Menu:")
    print("**********")
    print("\n".join(options))

def display_flights(flights):
    if not flights:
        print("\nNo flights found.")
        return
    
    headers = ["ID", "Origin", "OriginCode", "Destination", "DestinationCode", "Departure", "Arrival", "PilotID", "Status"]
    table = [list(flight) for flight in flights]

    table = [
        list(flight[:7]) + ["Needs Assigning" if flight[7] is None else flight[7]] + [flight[8]]
        for flight in flights
    ]
    
    print("\n" + tabulate.tabulate(table, headers=headers, tablefmt="grid"))

def display_summary(data, headers):
    if not data:
        print("\nNo data found.")
        return

    print("\n" + tabulate.tabulate(data, headers=headers, tablefmt="grid"))

def search_flights(db_ops):
    search_options = {
        "1": ("FlightOrigin", "OriginCode", "Enter Origin City or Airport Code: "),
        "2": ("FlightDestination", "DestinationCode", "Enter Destination City or Airport Code: "),
        "3": ("Status", None, "Choose Status:\n1. On Time\n2. Delayed\n3. Cancelled\nEnter choice (1-3): "),
        "4": ("Departure Time", None, "Enter Departure Time (YYYY-MM-DD or HH:MM): ")
    }
    
    print("\nSearch by:")
    for key, value in search_options.items():
        print(f"{key}. {value[2].split(':')[0]}")
    
    choice = input("Enter search option (1-4): ").strip()
    if choice not in search_options:
        print("Invalid selection.")
        return
    
    column, alt_column, prompt = search_options[choice]
    value = input(prompt).strip()
    
    if choice == "3":
        status_map = {"1": "On Time", "2": "Delayed", "3": "Cancelled"}
        value = status_map.get(value, "")
        if not value:
            print("Invalid selection.")
            return
    
    flights = db_ops.search_flights(column, value)
    if alt_column:
        flights += db_ops.search_flights(alt_column, value)
    
    display_flights(flights)

def assign_pilot(db_ops):
    flights = db_ops.retrieve_flights()
    if not flights:
        print("\nNo available flights.")
        return
    
    display_flights(flights)
    flight_id = input("\nEnter Flight ID to assign a pilot: ").strip()
    pilots = db_ops.get_available_pilots(flight_id)
    
    if not pilots:
        print("\nNo available pilots.")
        return
    
    print("\nAvailable Pilots:")
    for pilot in pilots:
        print(f"{pilot[0]} - {pilot[1]}")
    
    pilot_id = input("\nEnter Pilot ID: ").strip()
    if pilot_id not in [str(p[0]) for p in pilots]:
        print("Invalid selection.")
        return
    
    db_ops.assign_pilot(flight_id, pilot_id)
    print(f"\nPilot {pilot_id} assigned to Flight {flight_id}.")

def create_tables(db_ops):
    db_ops.create_tables()

def insert_flight(db_ops):
    db_ops.insert_flight()

def view_flights(db_ops):
    flights = db_ops.retrieve_flights()
    display_flights(flights)

def update_flight(db_ops):
    db_ops.update_flight()

def delete_flight(db_ops):
    db_ops.delete_flight()

def view_flights_per_destination(db_ops):
    data = db_ops.get_flights_per_destination()
    display_summary(data, ["Destination", "Airport Code", "Flight Count"])

def view_flights_per_pilot(db_ops):
    data = db_ops.get_flights_per_pilot()
    display_summary(data, ["Pilot ID", "Pilot Name", "Flight Count"])

# Dictionary for menu actions
menu_actions = {
    '1': create_tables,
    '2': insert_flight,
    '3': view_flights,
    '4': search_flights,
    '5': update_flight,
    '6': delete_flight,
    '7': assign_pilot,
    '8': view_flights_per_destination,
    '9': view_flights_per_pilot
}

def run_menu():
    db_ops = DBOperations()
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '10':
            print("Exiting application.")
            break
        elif choice in menu_actions:
            menu_actions[choice](db_ops)
        else:
            print("Invalid choice. Please select again.")