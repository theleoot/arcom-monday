import pandas as pd
from CODE.utils.dataframe.dataframe_relation import DataframeRelation

read = lambda file_path: pd.read_csv(file_path, encoding='latin-1', sep="\t")

# representante_dataframe = read("U:/PowerBI/Geral/representantes.csv")
# setor_dataframe = read("U:/PowerBI/Geral/setores.csv")

monitorado_dataframe = read("U:/PowerBI/Geral/clientes_monitorados.csv")
clientes_geral_dataframe = read("U:/PowerBI/Geral/clientes_geral.csv")
venda_mes_anterior_dataframe = read("U:/PowerBI/Mensal/notas202503.csv")

# register_dataframe = DataframeRelation(left_dataframe=representante_dataframe, left_key="representante", right_dataframe=setor_dataframe, right_key="Representante")

clientes_especiais_dataframe = DataframeRelation(
    left_dataframe=monitorado_dataframe,
    left_key="codCliente",
    right_dataframe=clientes_geral_dataframe,
    right_key="codCliente",
)

venda_mes_anterior_dataframe["vlrVdaSemIPI"] = venda_mes_anterior_dataframe["vlrVdaSemIPI"].str.replace(",", ".").astype(float)

group_last_month_sale = venda_mes_anterior_dataframe.query("tipoNF == 'VENDA'").groupby("codCliente")["vlrVdaSemIPI"].sum().reset_index()

filter = clientes_especiais_dataframe.search("respCliente == 'ANDRESSA DOS SANTOS ALVES GOMES'") # .to_csv("C:/Users/leonardo.tiago/Desktop/CLIENTS.csv", index=False)

clients_with_sales = pd.merge(group_last_month_sale, filter, on="codCliente", how="inner", validate="many_to_many")

# clients_with_sales.sort_values("vlrVdaSemIPI", ascending=False) # .to_csv("C:/Users/leonardo.tiago/Desktop/clientes_vendas.csv")

fields = [
    "vlrVdaSemIPI", "fantasiaRede_x", "dscRamoAtividade_x", "tipoMonitoramento_x",
    "estado_x", "cidade_x", "respCliente_x", "clienteChave_x", "dscRamoAtividade_y",
    "tipoMonitoramento_y", "cdm", "desc_cdm", "dddCelularCliente", "celularCliente"
]

fields_dict = {field: "max" for field in fields}

agg_sales = clients_with_sales.groupby("codRede_y").aggregate(fields_dict)

agg_sales.sort_values("vlrVdaSemIPI", ascending=False).to_csv("C:/Users/leonardo.tiago/Desktop/generated_data.csv", index=False)


