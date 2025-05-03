import monday
import pandas as pd
from typing import List, Dict, Any

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
    contact : str
        The contact name used when creating items

    Examples
    --------
    >>> handler = MondayDashboardHandler("your-api-key")
    >>> handler.create_item("John Smith", "example.com", "Jane Doe", "Deal 123", "Company description")
    """

    def __init__(self, api_key: str):
        """Initialize Monday client with API key"""
        self.client = monday.MondayClient(api_key)
        self.group_id = "topics"
        self.board_id = "8895172562"

    def create_item(self, contact: str, company_domain: str, account_contact: str, 
                   account_deal: str, company_description: str) -> Dict[str, Any]:
        """
        Create a new item in the Monday dashboard with the specified data.

        Parameters
        ----------
        contact : str
            Name of the contact to be used as the item name
        company_domain : str
            Domain of the company
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
        self.contact = contact

        column_values = {
            "text": company_domain,
            "text1": account_contact,
            "text2": account_deal,
            "long_text": company_description
        }
        
        try:
            response = self.client.items.create_item(
                board_id=self.board_id,
                item_name=self.contact,
                column_values=column_values,
                group_id=self.group_id
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to create item in Monday dashboard: {str(e)}")

    def create_multiple_items(self, items_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Create multiple items in batch.

        Parameters
        ----------
        items_data : List[Dict[str, str]]
            List of dictionaries containing item data.
            Each dictionary should have keys:
            - company_domain
            - account_contact
            - account_deal
            - company_description

        Returns
        -------
        List[Dict[str, Any]]
            List of API responses for each created item

        Examples
        --------
        >>> items = [
        ...     {
        ...         "company_domain": "example.com",
        ...         "account_contact": "John Doe",
        ...         "account_deal": "Deal 123",
        ...         "company_description": "Description"
        ...     }
        ... ]
        >>> handler.create_multiple_items(items)
        """
        responses = []
        for item in items_data:
            response = self.create_item(
                contact=self.contact,
                company_domain=item.get('company_domain', ''),
                account_contact=item.get('account_contact', ''),
                account_deal=item.get('account_deal', ''),
                company_description=item.get('company_description', '')
            )
            responses.append(response)
        return responses

cliets_handler = MondayDashboardHandler("eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUwNjA5ODU5OSwiYWFpIjoxMSwidWlkIjo3NDU0NDU5OSwiaWFkIjoiMjAyNS0wNC0yOVQxNDowMjoxOS4wNjhaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg5NzM1NjYsInJnbiI6InVzZTEifQ.A0vVD7CS3zGvFnF4VWuZYSoqyzE4T7zDv1wsm_Nobbk")

# cliets_handler.create_item("Test", "example.com", "John Doe", "Deal 123", "This is a test description")
cliets_handler.create_item("Test", "example.com", "John Doe", "Deal 123", "This is a test description")
