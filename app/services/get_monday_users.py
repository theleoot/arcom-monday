import os
from monday import MondayClient
from dataclasses import dataclass


@dataclass
class Users:
    client: MondayClient = MondayClient("eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUwNjA5ODU5OSwiYWFpIjoxMSwidWlkIjo3NDU0NDU5OSwiaWFkIjoiMjAyNS0wNC0yOVQxNDowMjoxOS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg5NzM1NjYsInJnbiI6InVzZTEifQ.0k3DE8V2o5grKALDpyGNiqBmLqA8N3fnsBma_WYpkjM")

    def get_all_user(self) -> list:
        user_data = []

        users = self.client.users.fetch_users()

        for user in users["data"]["users"]:
            user_data.append(
                {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "enabled": user["enabled"],
                }
            )
        
        return user_data

