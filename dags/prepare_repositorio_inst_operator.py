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

#---Unicode-----#
from unidecode import unidecode


class PrepareRepositorioInstitucional(BaseOperator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
    def execute(self, context):
        print('Preparing Repositorio Institucional')
        self.cleanData()
        
        
    def cleanData(self):
        institucional = pd.read_excel(f"{self.dag_path}/data/repositorio_inst/repositorio_inst_template.xlsx")
        isnt_columns=institucional.columns
        formatted_isnt_columns = [str(col).replace(" - ", "_") for col in isnt_columns]
        formatted_isnt_columns = [str(col).replace(".", "_") for col in formatted_isnt_columns]
        formatted_isnt_columns = [unidecode(str(col)) for col in formatted_isnt_columns]
        formatted_isnt_columns = [str(col).replace("ñ", "nn") for col in formatted_isnt_columns]
        rename_columns = dict(zip(isnt_columns, formatted_isnt_columns))    
        institucional=institucional.rename(columns=rename_columns)
        institucional.to_csv(f"{self.dag_path}/data/to_upload/rewrite/respositorio_inst.csv",index=False)
        
        