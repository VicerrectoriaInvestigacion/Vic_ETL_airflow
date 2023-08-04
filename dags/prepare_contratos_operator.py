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

class PrepareContratos(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
    def execute(self, context):
        print('Preparing contratos')
        self.cleanData()
        
        
    def cleanData(self):
       self.cleanContratos()
       
           
    def cleanContratos(self):
        contratos = pd.read_excel(f"{self.dag_path}/data/contratos/contratos_template.xlsx")
        contratos["ETL_upload_date"] = datetime.datetime.now()
        contratos.to_csv(f"{self.dag_path}/data/to_upload/rewrite/contratos.csv",index=False) 