from monday import MondayClient
from typing import Dict, Any

class MondayDashboardHandler:
    """
    A class to handle interactions with Monday.com dashboard.

    This class provides functionality to create and manage items in a Monday.com board,
    particularly focused on managing company and contact information.

    Parameters
    ----------
    api_key : str
        The API key for authenticating with Monday.com

    Attributes
    ----------
    client : monday.MondayClient
        The Monday.com client instance
    board_id : str
        The ID of the target Monday.com board
    group_id : str
        The ID of the group where items will be created
    """

    def __init__(self, api_key: str):
        """Initialize Monday client with API key"""
        self.client = MondayClient(api_key)
        self.board_id = "8895172235"
        self.group_id = "topics"

    def create_item(self, item_name: str, company_domain: str, account_contact: str,
                   account_deal: str, company_description: str) -> Dict[str, Any]:
        """
        Create a new item in the Monday dashboard with the specified data.

        Parameters
        ----------
        item_name : str
            Name of the item to be created
        company_domain : str
            Domain of the companyw
        account_contact : str
            Contact information
        account_deal : str
            Deal information
        company_description : str
            Description of the company

        Returns
        -------
        Dict[str, Any]
            Response from Monday API

        Raises
        ------
        RuntimeError
            If item creation fails
        """
        # Format the column values according to Monday.com's expected JSON structure
        column_values = {
            "text": {
                # "company_domain": company_domain,
                "account_contact": account_contact,
                # "account_deal": account_deal, 
                "headquarters_loc": company_description
            }
        }

        try:
            response = self.client.items.create_item(
                board_id=self.board_id,
                item_name=item_name,
                column_values=column_values,
                group_id=self.group_id,
                # create_labels_if_missing=True
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to create item in Monday dashboard: {str(e)}")

# Example usage:
monday_handler = MondayDashboardHandler("eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUwNjA5ODU5OSwiYWFpIjoxMSwidWlkIjo3NDU0NDU5OSwiaWFkIjoiMjAyNS0wNC0yOVQxNDowMjoxOS4wNjhaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg5NzM1NjYsInJnbiI6InVzZTEifQ.A0vVD7CS3zGvFnF4VWuZYSoqyzE4T7zDv1wsm_Nobbk")

# Create a sample item
monday_handler.create_item(
    item_name="Sample Company",
    company_domain="example.com",
    account_contact="John Doe",
    account_deal="Deal #123",
    company_description="This is a sample company description"
)

# api.items.create_item(board_id=8895172235, item_name="test", column_values={"company_description": "test", "company_domain": 'google.com google.com', "account_contact": '{\"name\" : \"My Item\"}'}, group_id="topics")