import json
import pandas as pd
from typing import Dict, Any

from monday import MondayClient


class MondayDashboardHandler:
    """
    A class to handle interactions with Monday.com dashboard.

    This class provides functionality to create and manage items in a Monday.com board,
    particularly focused on managing company and contact information.

    Parameters
    ----------
    api_key : str
        The API key for authenticating with Monday.com.

    Attributes
    ----------
    client : monday.MondayClient
        The Monday.com client instance.
    board_id : str
        The ID of the target Monday.com board.
    group_id : str
        The ID of the group where items will be created.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Monday client with the provided API key.

        Parameters
        ----------
        api_key : str
            The API key for Monday.com.
        """
        self.client = MondayClient(api_key)
        self.board_id = "8895172235"
        self.group_id = "topics"

    def create_item(self, item_name: str, **fields) -> Dict[str, Any]:
        """
        Create a new item in the Monday dashboard with the specified data.

        Parameters
        ----------
        item_name : str
            Name of the item to be created.
        **fields : dict
            Additional column values for the item.

        Returns
        -------
        Dict[str, Any]
            Response from the Monday API.

        Raises
        ------
        RuntimeError
            If item creation fails.
        """
        try:
            response = self.client.items.create_item(
                board_id=self.board_id,
                item_name=item_name,
                column_values=fields,
                group_id=self.group_id,
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to create item in Monday dashboard: {str(e)}")


# Example usage:
if __name__ == "__main__":
    # Replace with your actual API key
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUwNjA5ODU5OSwiYWFpIjoxMSwidWlkIjo3NDU0NDU5OSwiaWFkIjoiMjAyNS0wNC0yOVQxNDowMjoxOS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg5NzM1NjYsInJnbiI6InVzZTEifQ.0k3DE8V2o5grKALDpyGNiqBmLqA8N3fnsBma_WYpkjM"
    monday_handler = MondayDashboardHandler(api_key)

    # Create a sample item
    try:
        df = pd.read_csv("C:/Users/leonardo.tiago/OneDrive - Arcom SA/Área de Trabalho/PROJECTS/Monday Integration/CODE/DATA/_SELECT_TOP_1000_cvm_cliente_cvm_tipo_monitoramento_cvm_cliente__202504300928.csv")

        df = df.fillna("")

        clientes_andressa = df.to_numpy()

        for x in clientes_andressa:
            cliente, tipo, cliente_chave, usuario, razao, rede, associacao, nome_associacao = x

            check_associacao = "S" if associacao else "N"

            response = monday_handler.create_item(
                item_name=razao,
                multiple_person_mkpp7q97="74628342",
                numeric_mkqfswdp=cliente,
                numeric_mkqfj2fw=rede,
                numeric_mkqffepp=associacao,
                text_mkqgawwm=nome_associacao,
                dropdown_mkqf91nc=check_associacao
            )
        print("Items created successfully!")
    except RuntimeError as e:
        print(e)

