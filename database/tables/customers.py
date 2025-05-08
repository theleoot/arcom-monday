import sqlite3
from dataclasses import dataclass
from database.setup.connection import cur, con

from typing import Optional, Generator

@dataclass
class CustomerModel:
    id: int
    ramo_atividade: str
    board_id: str
    group_id: str
    data_sincronizacao_fonte: str
    data_atualizacao_monday: str
    codigo_cliente: int
    deleted: int = 0
    item_name: Optional[str] = None
    codigo_rede: Optional[int] = None
    codigo_associacao: Optional[int] = None
    nome_associacao: Optional[str] = None

class CustomersDatabase:
    def __init__(self, database_connection=cur):
        self.con = database_connection

    def create(self, **kwargs):
        customer_payload = CustomerModel(**kwargs).__dict__

        insert_query = """
            INSERT INTO customers (
                id, item_name, codigo_cliente, codigo_rede, codigo_associacao, 
                nome_associacao, ramo_atividade, board_id, group_id, 
                data_sincronizacao_fonte, data_atualizacao_monday, deleted
            ) VALUES (
                :id, :item_name, :codigo_cliente, :codigo_rede, :codigo_associacao, 
                :nome_associacao, :ramo_atividade, :board_id, :group_id, 
                :data_sincronizacao_fonte, :data_atualizacao_monday, :deleted
            )
        """

        con.execute(insert_query, customer_payload)
        con.commit()
        return customer_payload

    def get_one(self, customer_code: int):
        select_query = """
            SELECT * 
            FROM customers 
            WHERE codigo_cliente = :customer_code
        """
        cur.execute(select_query, {"customer_code": customer_code})
        return cur.fetchone()

    def customers_to_update(self) -> Generator[CustomerModel]:
        select_query = """
            SELECT * 
            FROM customers 
            WHERE 
                data_atualizacao_monday IS NULL
                OR data_sincronizacao_fonte IS NULL
                OR data_sincronizacao_fonte > data_atualizacao_monday
        """
        cur.execute(select_query)
        customers_fetch = cur.fetchall()

        for customer in customers_fetch:
            yield CustomerModel(
                id=customer[0],
                item_name=customer[1],
                codigo_cliente=customer[2],
                codigo_rede=customer[3],
                codigo_associacao=customer[4],
                nome_associacao=customer[5],
                ramo_atividade=customer[6],
                board_id=customer[7],
                group_id=customer[8],
                data_sincronizacao_fonte=customer[9],
                data_atualizacao_monday=customer[10],
                deleted=customer[11]
            ).__dict__
            
