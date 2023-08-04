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

class PrepareProyectos(BaseOperator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
        
    def execute(self, context):
        print('Reading Journals')
        self.cleanData()
        
  
    def cleanData(self):
        self.cleanProyectos()
        
        
    def cleanProyectos(self):
        proyectos = pd.read_excel(f"{self.dag_path}/data/proyectos/proyectos_template.xlsx")
        py_columns=proyectos.columns
        formatted_py_columns = [str(col).replace(" ", "_") for col in py_columns]
        formatted_py_columns = [str(col).replace(".", "_") for col in formatted_py_columns]
        formatted_py_columns = [unidecode(str(col)) for col in formatted_py_columns]
        rename_columns = dict(zip(py_columns, formatted_py_columns))
        proyectos=proyectos.rename(columns=rename_columns)
        proyectos.loc[(proyectos["VALOR_APROBADO_PATROCINADOR"]=="\\N"),"VALOR_APROBADO_PATROCINADOR"]=0
        proyectos["VALOR_APROBADO_PATROCINADOR"]=proyectos["VALOR_APROBADO_PATROCINADOR"].astype(float)
        proyectos['FECHA_DE_NEGOCIACION'] = proyectos['FECHA_DE_NEGOCIACION'].apply(lambda x: self._convert_to_datetime(x))
        proyectos["ETL_upload_date"] = datetime.datetime.now()
        proyectos.to_csv(f"{self.dag_path}/data/to_upload/rewrite/proyectos.csv",index=False)
            
            
    def _convert_to_datetime(self,value):
        if isinstance(value, int):
            return pd.to_datetime(str(value), format='%Y')
        else:
            return pd.to_datetime(value, errors='coerce')        