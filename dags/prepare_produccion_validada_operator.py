#---Airflow libraries-----#
import datetime
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#---JSON libraries-----#
import json

#---Elsapy libraries-----#
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
from elsapy.elssearch import ElsSearch

#---Pandas libraries-----#
import pandas as pd

#---Unicode-----#
from unidecode import unidecode

class PrepareProduccionValidada(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
    def execute(self, context):
        print('Preparing producción validada')
        self.cleanData()
        
        
    def cleanData(self):
        self.cleanProduccionValidada()
        
    
    def cleanProduccionValidada(self):
        produccion = pd.read_excel(f"{self.dag_path}/data/produccion_validada/produccion_validada_template.xlsx")
        pr_columns=produccion.columns
        formatted_pr_columns = [str(col).replace(" ", "_") for col in pr_columns]
        formatted_pr_columns = [str(col).replace("  ", "_") for col in formatted_pr_columns]
        formatted_pr_columns = [unidecode(str(col)) for col in formatted_pr_columns]
        formatted_pr_columns = [str(col).replace("ñ", "nn") for col in formatted_pr_columns]
        formatted_pr_columns = [str(col).replace("/", "_") for col in formatted_pr_columns]
        formatted_pr_columns = [str(col).replace("#", "num") for col in formatted_pr_columns]
        rename_columns = dict(zip(pr_columns, formatted_pr_columns))
        produccion=produccion.rename(columns=rename_columns)
        produccion.loc[(produccion["Tipo_documental"]=="Artículo"),"Tipo_documental"]="Articulo"
        produccion.loc[(produccion["Tipo_documental"]=="Article"),"Tipo_documental"]="Articulo"
        produccion.loc[(produccion["Tipo_documental"]=="Book Chapter"),"Tipo_documental"]="Capitulo de Libro"
        produccion.loc[(produccion["Tipo_documental"]=="Capítulo de libro"),"Tipo_documental"]="Capitulo de Libro"
        produccion.loc[(produccion["Tipo_documental"]=="Capitulo de libro"),"Tipo_documental"]="Capitulo de Libro"
        produccion.loc[(produccion["Tipo_documental"]=="Capítulo de Libro"),"Tipo_documental"]="Capitulo de Libro"
        produccion["ETL_upload_date"] = datetime.datetime.now()
        produccion.to_csv(f"{self.dag_path}/data/to_upload/rewrite/produccion_validada.csv",index=False)    
        