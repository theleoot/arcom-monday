import os
from monday import MondayClient


class Items:
    """
    A class to interact with and manage items on a Monday.com board.
    Parameters
    ----------
    board_id : str
        The unique identifier of the board to interact with.
    column_id : str, optional
        The unique identifier of the column to interact with (default is None).
    Methods
    -------
    get_column(search_value)
        Fetches items from the board based on a specific column value.
    update_values(replace_column_id, replace_column_value, search_value)
        Updates the values of items in a specified column based on a search value.
    """
    def __init__(self, token:str, board_id:str, column_id:str=None):
        self.client = MondayClient(token)
        self.board_id = board_id
        self.column_id = column_id

    def get_column(self, search_value):
        fetch_column = self.client.items.fetch_items_by_column_value(
            board_id=self.board_id,
            column_id=self.column_id,
            value=search_value
        )
        return fetch_column
    
    def get_by_id(self, item_id):
        fetch_column = self.client.items.fetch_items_by_id(
            value=item_id
        )
        return fetch_column

    def update_values(self, replace_column_id:str, replace_column_value:str, search_value:str):
        fetch_column_id = self.get_column(search_value)

        for item_data in fetch_column_id["data"]["items_page_by_column_values"]["items"]:
            self.client.items.change_item_value(
                board_id=self.board_id, 
                item_id=item_data["id"], 
                column_id=replace_column_id, 
                value=replace_column_value
            )

        return "Items Updated With Success!"