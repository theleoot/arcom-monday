import os
import pandas as pd # type: ignore
from dataclasses import dataclass

@dataclass
class FileInfo:
    base_path = "C:/Users/leonardo.tiago/Desktop/Monday Integration/"
    file_list = ["clientes_geral.csv", "clientes_monitorados.csv"]
    columns_to_show = ['codCliente', 'fantasiaCliente',  'dscRamoAtividade', 'tipoMonitoramento', 'estado', 'cidade', 'respCliente', 'clienteChave']

clientes_geral = pd.read_csv("C:/Users/leonardo.tiago/Desktop/Monday Integration/clientes_geral.csv", encoding="latin-1", sep="\t")
clientes_monitorados = pd.read_csv("C:/Users/leonardo.tiago/Desktop/Monday Integration/clientes_monitorados.csv", encoding="latin-1", sep="\t")

special_clientes = clientes_monitorados.query("clienteChave == 'S'").head(100)["codCliente"].to_list()

special_clients_data = clientes_geral[clientes_geral["codCliente"].isin(special_clientes)][
    [
        'codCliente', 
        'fantasiaCliente', 
        'dscRamoAtividade', 
        'tipoMonitoramento', 
        'estado', 
        'cidade', 
        'respCliente',  
        'clienteChave', 
        'ocorrencia', 
        'ocorCadastro', 
        'emailCliente', 
        'dddCelularCliente', 
        'celularCliente',  
        'dddTelefoneCliente', 
        'telefoneCliente'
    ]]

special_clients_data.fillna(value="", inplace=True)

special_clients_data["dddCelularCliente"] = special_clients_data["dddCelularCliente"].astype(str).map(lambda x: x.split(".")[0])
special_clients_data["celularCliente"] = special_clients_data["celularCliente"].astype(str).map(lambda x: x.split(".")[0])
                                                       
special_clients_data["dddTelefoneCliente"] = special_clients_data["dddTelefoneCliente"].astype(str).map(lambda x: x.split(".")[0])
special_clients_data["telefoneCliente"] = special_clients_data["telefoneCliente"].astype(str).map(lambda x: x.split(".")[0])                                                  

special_clients_data["Celular"] = special_clients_data["dddCelularCliente"] + special_clients_data["celularCliente"]
special_clients_data["Telefone"] = special_clients_data["dddTelefoneCliente"] + special_clients_data["telefoneCliente"]

special_clients_data.to_csv("C:/Users/leonardo.tiago/Desktop/Monday Integration/contacts.csv", index=False)