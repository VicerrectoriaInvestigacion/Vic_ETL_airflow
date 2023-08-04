#---Airflow libraries-----#
import datetime
import glob
import json
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#---Pandas libraries-----#
import pandas as pd


class PrepareRevistas(BaseOperator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
        
    def execute(self, context):
        print('Reading Revistas')
        self.cleanData()
        
  
    def cleanData(self):
        self.cleanRevistas()
    
    
    def cleanRevistas(self):
        revistas = pd.read_excel(f"{self.dag_path}/data/revistas/revistas_template.xlsx")
        revistas=revistas.rename(columns={"Año2":"Year","Nombre revista":"Name","Fuente":"Source","Categoria":"Category"})
        rv_columns=revistas.columns
        formatted_rv_columns = [str(col).replace(" ", "_") for col in rv_columns]
        rename_columns = dict(zip(rv_columns, formatted_rv_columns))
        revistas=revistas.rename(columns=rename_columns)
        revistas["ETL_upload_date"] = datetime.datetime.now()
        revistas.to_csv(f"{self.dag_path}/data/to_upload/append/revistas.csv",index=False)  
        
   