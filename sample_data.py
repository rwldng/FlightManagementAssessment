# Sample pilot, destination, and flight data to populate the tables

from db_operations import DBOperations

def populate_sample_data():
    db_ops = DBOperations()

    try:
        # Sample pilots
        pilots = [
            ("Olivia Hunter"), ("Jane King"), ("Neville Anderson"),
            ("Lily Matisse"), ("Adam White"), ("Des Green"),
            ("Neil Princeton"), ("Sophia White"), ("James Taylor"),
            ("Daniel Wilson")
        ]

        for name in pilots:
            db_ops.cur.execute("INSERT OR IGNORE INTO Pilots (Name) VALUES (?)", (name,))

        # Sample destinations
        destinations = [
            ("London", "LGW"), ("Amsterdam", "AMS"), ("Marrakech", "RAK"),
            ("San Diego", "SAN"), ("Los Angeles", "LAX"), ("Berlin", "BER"),
            ("Newark", "EWR"), ("Budapest", "BUD"), ("Cologne", "CGN"),
            ("Gibraltar", "GIB"), ("Barcelona", "BCN"), ("Dublin", "DUB"),
            ("Prague", "PRG"), ("Athens", "ATH"), ("Oslo", "OSL")
        ]

        for city, airport_code in destinations:
            db_ops.cur.execute("INSERT OR IGNORE INTO Destinations (City, AirportCode) VALUES (?, ?)", (city, airport_code))

        # Sample flight data
        flights = [
            ("London", "LGW", "Marrakech", "RAK", "2025-03-01 08:00", "2025-03-01 12:00", "On Time"),
            ("Amsterdam", "AMS", "San Diego", "SAN", "2025-03-02 09:30", "2025-03-02 18:45", "Delayed"),
            ("San Diego", "SAN", "Los Angeles", "LAX", "2025-03-03 12:00", "2025-03-03 13:00", "On Time"),
            ("Berlin", "BER", "Newark", "EWR", "2025-03-04 15:00", "2025-03-04 22:30", "On Time"),
            ("Budapest", "BUD", "Cologne", "CGN", "2025-03-05 06:00", "2025-03-05 08:15", "On Time"),
            ("Cologne", "CGN", "Gibraltar", "GIB", "2025-03-06 09:45", "2025-03-06 14:30", "Delayed"),
            ("Barcelona", "BCN", "Dublin", "DUB", "2025-03-07 17:20", "2025-03-07 19:50", "On Time"),
            ("Prague", "PRG", "Athens", "ATH", "2025-03-08 13:10", "2025-03-08 16:30", "On Time"),
            ("Athens", "ATH", "Oslo", "OSL", "2025-03-09 22:00", "2025-03-10 02:45", "Cancelled"),
            ("Los Angeles", "LAX", "London", "LGW", "2025-03-10 19:00", "2025-03-11 11:30", "On Time"),
            ("Berlin", "BER", "Oslo", "OSL", "2025-03-05 06:00", "2025-03-05 09:30", "On Time"),
            ("Budapest", "BUD", "Gibraltar", "GIB", "2025-03-05 06:00", "2025-03-05 10:15", "On Time")
        ]

        for flight in flights:
            db_ops.cur.execute("""
                INSERT OR IGNORE INTO FlightInfo 
                (FlightOrigin, OriginCode, FlightDestination, DestinationCode, DepartureTime, ArrivalTime, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, flight)

        db_ops.conn.commit()
        print("Sample data inserted successfully")

    finally:
        db_ops.close_connection()

if __name__ == "__main__":
    populate_sample_data()