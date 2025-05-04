from dataclasses import dataclass
import sqlite3
from database.setup.connection import cur, con

@dataclass
class UserModel:
    id: int
    user_name: str
    monday_name: str
    monday_id: int
    role: str

class UsersDatabase:
    """
    A class used to represent the Users table in the database.
    Parameters
    ----------
    database_connection : object
        A database connection object used to interact with the database.
    Methods
    -------
    some()
        A placeholder method that returns a string "some".
    """
    def __init__(self, database_connection=cur):
        self.con = database_connection
    
    def create(self, id: int, user_name: str, monday_name: str, monday_id: int, role: str):
            user_payload = {
                "id": id,
                "user_name": user_name,
                "monday_name": monday_name,
                "monday_id": monday_id,
                "role": role,
            }

            insert_query = """
                INSERT INTO 
                users (id, name, monday_id, monday_name, role)
                VALUES (:id, :user_name, :monday_id, :monday_name, :role)
            """

            try:
                self.con.execute(insert_query, user_payload)
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: users.id":
                    print(f"User with ID {id} already exists.")

            con.commit()
