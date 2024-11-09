# Descriptions:
"""
Create a tool which will calculate straight-line distance between different cities based on coordinates:
 1. User will provide two city names by console interface
 2. If tool do not know about city coordinates, it will ask user for input and store it in SQLite
  database for future use
 3. Return distance between cities in kilometers
Do not forgot that Earth is a sphere, so length of one degree is different.
"""

import math
import sqlite3


class DBProcessor:
    """Manages the SQLite database for city coordinates."""

    def __init__(self, p_db_name: str = 'cities.db'):
        self.db_name = p_db_name
        self.cities_table = 'cities_coordinates'
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()  # Initialize tables on startup

    def create_tables(self):
        """Creates table if it does not exist."""
        cities_tbl_create_script = """
            CREATE TABLE IF NOT EXISTS city_coordinates (
                city_name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        """
        # Creating table
        self.cursor.execute(cities_tbl_create_script)
        self.connection.commit()  # Commit table creation

    def get_db_city_coordinates(self, city_name):
        """Fetch coordinates for a city if it exists in the database."""
        self.cursor.execute("""
            SELECT latitude, longitude FROM city_coordinates WHERE upper(city_name) = ?
            """, (city_name.upper(),))
        return self.cursor.fetchone()

    def save_city_coordinates(self, city_name, latitude, longitude):
        """Store coordinates for a new city."""
        self.cursor.execute("INSERT OR REPLACE INTO city_coordinates (city_name, latitude, longitude) VALUES (?, ?, ?)",
                            (city_name, latitude, longitude))
        self.connection.commit()

    def close(self):
        """Closes the database connection."""
        self.connection.close()


class DistanceCalculation:
    """Calculates the straight-line distance between cities using the Haversine formula."""
    def __init__(self):
        self.db_processor = DBProcessor()

    def get_city_coordinates(self, city_name: str):
        """Get city coordinates from DB or ask user to enter."""
        coordinates = self.db_processor.get_db_city_coordinates(city_name)
        if not coordinates:
            print(f"Coordinates for {city_name} not found.")
            latitude = float(input(f"Enter latitude for {city_name} (e.g., 34.0522 for Los Angeles): "))
            longitude = float(input(f"Enter longitude for {city_name} (e.g., -118.2437 for Los Angeles): "))
            self.db_processor.save_city_coordinates(city_name, latitude, longitude)
            coordinates = (latitude, longitude)
        return coordinates

    @staticmethod
    def calculate_haversine(lat1, lon1, lat2, lon2):
        """Calculate distance in kilometers between two latitude/longitude pairs."""
        r = 6371.0  # Earth's radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    def calculate_distance(self, city1, city2):
        """Calculate distance between two cities."""
        lat1, lon1 = self.get_city_coordinates(city1)
        lat2, lon2 = self.get_city_coordinates(city2)
        return self.calculate_haversine(lat1, lon1, lat2, lon2)

    def close(self):
        """Closes the database connection through the manager."""
        self.db_processor.close()


def main():
    """Main function to determine how to process publications: console or file."""

    print("\nWelcome to the distance_calculator!")
    calculator = DistanceCalculation()
    try:
        city1 = input("Enter the first city name: ")
        city2 = input("Enter the second city name: ")
        distance = calculator.calculate_distance(city1, city2)
        print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} km.")
    finally:
        calculator.close()  # Ensure the database connection is closed


if __name__ == "__main__":
    main()
