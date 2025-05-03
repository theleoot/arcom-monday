from dataclasses import dataclass

import pandas as pd
from monday import MondayClient


@dataclass
class MondayDashboardData:
    def __init__(self, token: str):
        self.token: str = token
        self.client: MondayClient = MondayClient(token)
    
    @property
    def items(self):
        return self.client.items
    
    @property
    def boards(self):
        return self.client.boards
    
    def get_board(self, board_id: str):
        board_search = self.boards.fetch_boards_by_id(board_id)
        return board_search

clients_board = MondayDashboardData("eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUwNjA5ODU5OSwiYWFpIjoxMSwidWlkIjo3NDU0NDU5OSwiaWFkIjoiMjAyNS0wNC0yOVQxNDowMjoxOS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg5NzM1NjYsInJnbiI6InVzZTEifQ.0k3DE8V2o5grKALDpyGNiqBmLqA8N3fnsBma_WYpkjM")

board_data = clients_board.get_board("8895172235")
print(board_data)