import os
from dataclasses import dataclass

from monday import MondayClient


@dataclass
class MondayDashboardData:
    def __init__(self, token=os.getenv("MONDAY_API_KEY")):
        self.token: str = token
        self.client: MondayClient = MondayClient(token)
    
    @property
    def items(self):
        return self.client.items
    
    @property
    def boards(self):
        return self.client.boards
    
    def get_board(self, board_id: str, group_id: str):
        board_search = self.boards.fetch_items_by_board_id(board_id, group_id)
        return board_search
    
    def get_item(self, item_id: str):
        item_search = self.items.fetch_items_by_id(item_id)
        return item_search