import requests


class Monday:
    """
    A class to interact with the Monday.com API.

    Parameters
    ----------
    api_key : str
        Your Monday.com API key.

    Attributes
    ----------
    api_key : str
        The API key used for authentication.
    base_url : str
        The base URL for the Monday.com API.

    Methods
    -------
    get_dashboard(dashboard_id: int) -> dict
        Fetches dashboard data for the given dashboard ID.
    get_board_items(board_ids: list[int]) -> dict
        Fetches board items for the given list of board IDs.
    normalize_board_items(board_response: dict) -> dict
        Normalizes the board response into a dictionary of item IDs and names.
    normalize_data(data: dict) -> generator
        Normalizes the board items data into a generator of dictionaries.
    clientes() -> list[dict]
        Fetches and normalizes client data from a specific dashboard.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.monday.com/v2"

    def _api_post(self, query: str) -> dict:
        """
        Sends a POST request to the Monday.com API.

        Parameters
        ----------
        query : str
            The GraphQL query to execute.

        Returns
        -------
        dict
            The JSON response from the API.
        """
        response = requests.post(
            self.base_url,
            json={"query": query},
            headers={"Authorization": self.api_key},
        )
        response.raise_for_status()
        return response.json()

    def get_dashboard(self, dashboard_id: int) -> dict:
        """
        Fetches dashboard data for the given dashboard ID.

        Parameters
        ----------
        dashboard_id : int
            The ID of the dashboard to fetch.

        Returns
        -------
        dict
            The dashboard data.

        Raises
        ------
        ValueError
            If the dashboard_id is not an integer.
        """
        if not isinstance(dashboard_id, int):
            raise ValueError("The dashboard_id must be an integer!")

        query = f"""
        {{
            boards(ids: {dashboard_id}) {{
                items_page(limit: 100) {{
                    cursor
                    items {{
                        id
                        name
                    }}
                }}
            }}
        }}
        """
        return self._api_post(query=query)

    def get_board_items(self, board_ids: list[int]) -> dict:
        """
        Fetches board items for the given list of board IDs.

        Parameters
        ----------
        board_ids : list[int]
            A list of board IDs to fetch items for.

        Returns
        -------
        dict
            The board items data.
        """
        board_ids_str = ", ".join(map(str, board_ids))
        query = f"""
        query {{
            items(ids: [{board_ids_str}]) {{
                id
                name
                column_values {{
                    id
                    text
                    ... on BoardRelationValue {{
                        linked_item_ids
                        linked_items {{
                            id
                            name
                            column_values {{
                                id
                                __typename
                                text
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        return self._api_post(query=query)

    @staticmethod
    def normalize_board_items(board_response: dict) -> dict:
        """
        Normalizes the board response into a dictionary of item IDs and names.

        Parameters
        ----------
        board_response : dict
            The raw board response from the API.

        Returns
        -------
        dict
            A dictionary mapping item IDs to their names.
        """
        items = board_response["data"]["boards"][0]["items_page"]["items"]
        return {int(item["id"]): item["name"] for item in items}

    @staticmethod
    def normalize_data(data: dict):
        """
        Normalizes the board items data into a generator of dictionaries.

        Parameters
        ----------
        data : dict
            The raw board items data from the API.

        Yields
        ------
        dict
            A dictionary containing normalized data for each item.
        """
        for item in data["data"]["items"]:
            yield {
                column["id"]: column["text"]
                for column in item["column_values"]
            } | {"name": item["name"], "id": item["id"]}

    def clientes(self) -> list[dict]:
        """
        Fetches and normalizes client data from a specific dashboard.

        Returns
        -------
        list[dict]
            A list of dictionaries containing normalized client data.
        """
        dashboard_id = 8895172235 # 8799470231
        dashboard_items_response = self.get_dashboard(dashboard_id)
        normalized_dashboard_items = self.normalize_board_items(dashboard_items_response)
        board_items_response = self.get_board_items(list(normalized_dashboard_items.keys()))
        
        return list(self.normalize_data(board_items_response))