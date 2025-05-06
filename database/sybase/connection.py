import pyodbc

# Substitua os valores conforme seu ambiente
conn = pyodbc.connect(
    'DRIVER={Adaptive Server Enterprise};'
    'SERVER=terra.arcom.com.br;'
    'PORT=4101;'
    'DATABASE=Vendas;'
    'UID=leonardo;'
    'PWD=RLqw72ypBQCN'
)

cursor = conn.cursor()

find_associations_query = """
    SELECT 
        a.associacao,
        a.desc_associacao,
        COUNT(ac.cliente) as quantidade_clientes,
        MAX(ac.data_inicio) as data_ultimo_cliente_adicionado
    FROM
        vendas.dbo.associacoes a
    LEFT JOIN
        vendas.dbo.associacao_clientes ac
        ON
        a.associacao = ac.associacao
    GROUP BY 
        a.associacao,
        a.desc_associacao,
        a.observacao;
"""

database_response = cursor.execute(find_associations_query)

conn.close()

print(database_response)
