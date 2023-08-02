#---Airflow libraries-----#
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

#---Time-----#
import datetime

#---Unicode-----#
from unidecode import unidecode


class PrepareProfesoresValidados(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
    def execute(self, context):
        print('Preparing Profesores validados')
        self.cleanData()
        
        
    def cleanData(self):
       self.cleanProfesoresValidados()
       self.cleanScopusIdsProfesoresValidados()
        
       
 
       
    def cleanProfesoresValidados(self):
        
        profesores = pd.read_excel(f"{self.dag_path}/data/profesores_validados/profesores_validados_template.xlsx")
        pr_columns=profesores.columns
        formatted_pr_columns = [str(col).replace(" ", "_") for col in pr_columns]
        formatted_pr_columns = [str(col).replace("ñ", "nn") for col in formatted_pr_columns]
        formatted_pr_columns = [unidecode(str(col)) for col in formatted_pr_columns]
        
        rename_columns = dict(zip(pr_columns, formatted_pr_columns))
        profesores=profesores.rename(columns=rename_columns)
        profesores.drop(columns=["SCOPUS_AUTHOR_ID"],inplace=True)
        profesores["ETL_upload_date"] = datetime.datetime.now()
        profesores.to_csv(f"{self.dag_path}/data/to_upload/rewrite/profesores_validados.csv",index=False)
        
    
    def cleanScopusIdsProfesoresValidados(self): 
        profesores_scopus_ids = pd.read_excel(f"{self.dag_path}/data/profesores_validados/profesores_validados_scopus_ids_template.xlsx")
        profesores_scopus_ids_columns=profesores_scopus_ids.columns
        formatted_pr_columns = [str(col).replace(" ", "_") for col in profesores_scopus_ids_columns]
        rename_columns = dict(zip(profesores_scopus_ids_columns, formatted_pr_columns))
        profesores_scopus_ids=profesores_scopus_ids.rename(columns=rename_columns)
        profesores_scopus_ids["ETL_upload_date"] = datetime.datetime.now()
        profesores_scopus_ids.to_csv(f"{self.dag_path}/data/to_upload/rewrite/profesores_validados_scopus_ids.csv",index=False) 