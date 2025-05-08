import sqlite3

con = sqlite3.connect("C:/Users/leonardo.tiago/OneDrive - Arcom SA/PROGRAMS/arcom-monday/database/database/monday.db")
cur = con.cursor()

class CustomersMigration:
    def __init__(self, db):
        self.db = db

    def create_customers_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                item_name TEXT,
                codigo_cliente INT NOT NULL UNIQUE,
                codigo_rede INT,
                codigo_associacao INT,
                nome_associacao TEXT,
                ramo_atividade TEXT,
                board_id INT NOT NULL,
                group_id INT NOT NULL,
                data_sincronizacao_fonte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao_monday TIMESTAMP,
                deleted INTEGER DEFAULT 0
            )
        """)
        self.db.commit()

    def drop_customers_table(self):
        self.db.execute("DROP TABLE IF EXISTS customers")
        self.db.commit()