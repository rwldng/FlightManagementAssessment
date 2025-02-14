# Stores the SQL queries for the Flight Management System database

CREATE_DESTINATIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS Destinations (
        DestinationID INTEGER PRIMARY KEY AUTOINCREMENT,
        City TEXT NOT NULL,
        AirportCode TEXT NOT NULL UNIQUE
    )
    """

CREATE_PILOTS_TABLE = """
    CREATE TABLE IF NOT EXISTS Pilots (
        PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    )
    """

CREATE_FLIGHTS_TABLE = """
    CREATE TABLE IF NOT EXISTS FlightInfo (
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
        FlightOrigin TEXT NOT NULL,
        OriginCode TEXT NOT NULL,
        FlightDestination TEXT NOT NULL,
        DestCode TEXT NOT NULL,
        DepartureTime TEXT NOT NULL,
        ArrivalTime TEXT NOT NULL,
        PilotID INTEGER,
        Status TEXT CHECK(Status IN ('On Time', 'Delayed', 'Cancelled')) NOT NULL,
        FOREIGN KEY (FlightOrigin) REFERENCES Destinations(City),
        FOREIGN KEY (FlightDestination) REFERENCES Destinations(City),
        FOREIGN KEY (PilotID) REFERENCES Pilots(PilotID)
    )
    """

INSERT_FLIGHT = """
    INSERT INTO FlightInfo (FlightOrigin, OriginCode, FlightDestination, DestCode, DepartureTime, ArrivalTime, Status) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

UPDATE_FLIGHT = """
    UPDATE FlightInfo 
    SET DepartureTime = ?, ArrivalTime = ?, Status = ? 
    WHERE FlightID = ?
    """

DELETE_FLIGHT = "DELETE FROM FlightInfo WHERE FlightID = ?"

SEARCH_FLIGHTS = {
        "1": "SELECT * FROM FlightInfo WHERE FlightOrigin LIKE ?",
        "2": "SELECT * FROM FlightInfo WHERE FlightDestination LIKE ?",
        "3": "SELECT * FROM FlightInfo WHERE Status LIKE ?",
        "4": "SELECT * FROM FlightInfo WHERE DepartureTime LIKE ?"
    }

GET_AVAILABLE_PILOTS = """
    SELECT p.PilotID, p.Name 
    FROM Pilots p
    WHERE NOT EXISTS (
        SELECT 1 FROM FlightInfo f
        WHERE f.PilotID = p.PilotID
        AND (
            (f.DepartureTime BETWEEN ? AND ?)
            OR (f.ArrivalTime BETWEEN ? AND ?)
            OR (? BETWEEN f.DepartureTime AND f.ArrivalTime)
            OR (? BETWEEN f.DepartureTime AND f.ArrivalTime)
        )
    )
    """

ASSIGN_PILOT = "UPDATE FlightInfo SET PilotID = ? WHERE FlightID = ?"

FLIGHTS_PER_DESTINATION = """
    SELECT FlightDestination, DestinationCode, COUNT(*) AS FlightCount
    FROM FlightInfo
    GROUP BY FlightDestination, DestinationCode
    ORDER BY FlightCount DESC;
    """

FLIGHTS_PER_PILOT = """
    SELECT p.PilotID, p.Name, COUNT(f.FlightID) AS FlightCount
    FROM Pilots p
    LEFT JOIN FlightInfo f ON p.PilotID = f.PilotID
    GROUP BY p.PilotID, p.Name
    ORDER BY FlightCount DESC;
    """