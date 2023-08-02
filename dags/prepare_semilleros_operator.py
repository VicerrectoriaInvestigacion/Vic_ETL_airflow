#---Airflow libraries-----#
import datetime
import glob
import json
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#---Pandas libraries-----#
import pandas as pd

#---Unicode-----#
from unidecode import unidecode

class PrepareSemilleros(BaseOperator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
        
    def execute(self, context):
        print('Reading Semilleros')
        self.cleanData()
        
  
    def cleanData(self):
        self.cleanSemilleros()
    
    
    def cleanSemilleros(self):
        semilleros = pd.read_excel(f"{self.dag_path}/data/semilleros/semilleros_template.xlsx")
        sm_columns=semilleros.columns
        formatted_sm_columns = [str(col).replace(" ", "_") for col in sm_columns]
        formatted_sm_columns = [str(col).replace("/", "_") for col in formatted_sm_columns]
        formatted_sm_columns = [unidecode(str(col)) for col in formatted_sm_columns]
        rename_columns = dict(zip(sm_columns, formatted_sm_columns))
        semilleros=semilleros.rename(columns=rename_columns)
        semilleros.to_csv(f"{self.dag_path}/data/to_upload/rewrite/semilleros.csv",index=False)  