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


class PrepareProfesoresData(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
    def execute(self, context):
        print('Preparing Profesores Core Data')
        self.cleanData()
        
        
    def cleanData(self):
      
      self.cleanProfesoresCoreData()
      self.cleanProfesoresHijosData()
      self.cleanProfesoresFormacionData()
       
 
       
    def cleanProfesoresCoreData(self):
        data_types = {'ID': str}
        profesores = pd.read_excel(f"{self.dag_path}/data/profesores_data/profesores_core_template.xlsx",dtype=data_types)
        profesores["ID"]="ID"+profesores["ID"]
        pr_columns=profesores.columns
        formatted_pr_columns = [str(col).replace(" ", "_") for col in pr_columns]
        rename_columns = dict(zip(pr_columns, formatted_pr_columns))
        profesores=profesores.rename(columns=rename_columns)
        profesores["ETL_upload_date"] = datetime.datetime.now()
        profesores.to_csv(f"{self.dag_path}/data/to_upload/rewrite/profesores_core_data.csv",index=False)
        

    def cleanProfesoresHijosData(self):
        data_types = {'EMPLID': str}
        profesores_hijos = pd.read_excel(f"{self.dag_path}/data/profesores_data/profesores_hijos_template.xlsx",dtype=data_types)
        profesores_hijos["EMPLID"]="ID"+profesores_hijos["EMPLID"]
        pr_h_columns=profesores_hijos.columns
        formatted_pr_h_columns = [str(col).replace(" ", "_") for col in pr_h_columns]
        formatted_pr_h_columns = [str(col).replace(".", "_") for col in formatted_pr_h_columns]
        rename_columns = dict(zip(pr_h_columns, formatted_pr_h_columns))
        profesores_hijos=profesores_hijos.rename(columns=rename_columns)
        profesores_hijos["ETL_upload_date"] = datetime.datetime.now()
        profesores_hijos.to_csv(f"{self.dag_path}/data/to_upload/rewrite/profesores_hijos.csv",index=False)   


    def cleanProfesoresFormacionData(self):
        data_types = {'EMPLID': str}
        profesores_formacion = pd.read_excel(f"{self.dag_path}/data/profesores_data/profesores_formacion_template.xlsx",dtype=data_types)
        profesores_formacion["EMPLID"]="ID"+profesores_formacion["EMPLID"]
        profesores_formacion["ETL_upload_date"] = datetime.datetime.now()
        profesores_formacion.to_csv(f"{self.dag_path}/data/to_upload/append/profesores_formacion.csv",index=False) 