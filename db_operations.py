# Handles interactions with the database for the Flight Management System

import sqlite3
from datetime import datetime
from queries import *

class DBOperations:
    def __init__(self):
        self.conn = sqlite3.connect("FlightManagement.db")
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Creates tables if they don’t already exist
        self.cur.execute(CREATE_DESTINATIONS_TABLE)
        self.cur.execute(CREATE_PILOTS_TABLE)
        self.cur.execute(CREATE_FLIGHTS_TABLE)
        self.conn.commit()

    def retrieve_flights(self):
        self.cur.execute("SELECT * FROM FlightInfo")
        return self.cur.fetchall()

    def search_flights(self, column, value):
        valid_columns = ["FlightOrigin", "OriginCode", "FlightDestination", "DestinationCode", "Status", "DepartureTime"]
        if column not in valid_columns:
            print("Invalid search column.")
            return []

        self.cur.execute(f"SELECT * FROM FlightInfo WHERE LOWER({column}) LIKE LOWER(?)", (f"%{value}%",))
        return self.cur.fetchall()

    def insert_flight(self):
        fields = ["Origin City", "Origin Airport Code", "Destination City", "Destination Airport Code", 
                  "Departure Time (YYYY-MM-DD HH:MM)", "Arrival Time (YYYY-MM-DD HH:MM)", "Status (On Time, Delayed, Cancelled)"]
        values = [input(f"Enter {field}: ").strip() for field in fields]
        self.cur.execute(INSERT_FLIGHT, values)
        self.conn.commit()
        print("Flight added")

    def update_flight(self):
        flight_id = input("Enter Flight ID to update: ").strip()

        def validate_datetime(prompt):
            while True:
                value = input(prompt).strip()
                try:
                    return datetime.strptime(value, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    print("Incorrect format. Please enter in 'YYYY-MM-DD HH:MM'")
        departure_time = validate_datetime("Enter new departure time (YYYY-MM-DD HH:MM): ")
        arrival_time = validate_datetime("Enter new arrival time (YYYY-MM-DD HH:MM): ")

        status_options = {"1": "ON TIME", "2": "DELAYED", "3": "CANCELLED"}
        print("\nChoose new status:")
        for key, value in status_options.items():
            print(f"{key}. {value}")

        status_choice = input("Enter choice (1-3): ").strip()
        status = status_options.get(status_choice, None)

        if not status:
            print("Invalid selection")
            return

        self.cur.execute(UPDATE_FLIGHT, (departure_time, arrival_time, status, flight_id))
        self.conn.commit()
        print("Flight updated")

    def delete_flight(self):
        flight_id = input("Enter Flight ID to delete: ").strip()
        self.cur.execute(DELETE_FLIGHT, (flight_id,))
        self.conn.commit()
        print("Flight deleted")

    def get_available_pilots(self, flight_id):
        # Pilots who are not already assigned at that time
        self.cur.execute("SELECT DepartureTime, ArrivalTime FROM FlightInfo WHERE FlightID = ?", (flight_id,))
        flight_time = self.cur.fetchone()

        if not flight_time:
            print("Invalid Flight ID.")
            return []

        departure_time, arrival_time = flight_time
        self.cur.execute(GET_AVAILABLE_PILOTS, (departure_time, arrival_time, departure_time, arrival_time, departure_time, arrival_time))
        return self.cur.fetchall()

    def assign_pilot(self, flight_id, pilot_id):
        self.cur.execute(ASSIGN_PILOT, (pilot_id, flight_id))
        self.conn.commit()
        print(f"Pilot {pilot_id} assigned to Flight {flight_id}.")

    def get_flights_per_destination(self):
        self.cur.execute(FLIGHTS_PER_DESTINATION)
        return self.cur.fetchall()

    def get_flights_per_pilot(self):
        self.cur.execute(FLIGHTS_PER_PILOT)
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()