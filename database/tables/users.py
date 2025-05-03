class Users:
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
    def __init__(self, database_connection):
        self.con = database_connection
    
    def some(self):
        return "some"