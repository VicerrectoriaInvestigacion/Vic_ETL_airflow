#---Airflow libraries-----#
import datetime
import glob
import json
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#---Pandas libraries-----#
import pandas as pd


from google.oauth2 import service_account
from google.cloud import bigquery

class ExportData(BaseOperator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
        self.credentials = service_account.Credentials.from_service_account_file(
            f"{self.dag_path}/data/bigQuery/viceinvestigacion-7d7d86b22e96.json",
            scopes = ["https://www.googleapis.com/auth/cloud-platform"])
        
        self.client = bigquery.Client(credentials = self.credentials, project = self.credentials.project_id)
        
    def execute(self, context):
        print('Exporting Data')
        self.export_data(exportingType="rewrite")
        self.export_data(exportingType="append")
       
        
    
    def createTable(self,tableName, df,schema,write_disposition="WRITE_TRUNCATE"):
        dataset_id = 'socupus_data'
        table_id = tableName
        full_table_id = f'{self.client.project}.{dataset_id}.{table_id}' 
        if schema!=None:
            load_job_config = bigquery.LoadJobConfig(write_disposition = write_disposition,schema=schema)
         
        else:
            load_job_config = bigquery.LoadJobConfig(write_disposition = write_disposition)    
            
        job= self.client.load_table_from_dataframe(df,full_table_id,job_config=load_job_config)
        print(job.result())
    
    
    def export_data(self, exportingType="rewrite"):
        
        if(exportingType=="rewrite"):
            folder_path = f"{self.dag_path}/data/to_upload/rewrite"   
            write_disposition="WRITE_TRUNCATE"  ## Sobrescribe
        else:
            folder_path = f"{self.dag_path}/data/to_upload/append"    
            write_disposition="WRITE_APPEND" ## Concatena
            
        
        file_paths = glob.glob(os.path.join(folder_path, '*'))
        for file_path in file_paths:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            print(f"📝File name: {file_name}, File Path: ${file_path}")
            df = pd.read_csv(file_path,low_memory=False)
            try:
                self.createTable(file_name,df,None,write_disposition=write_disposition)
            except:
                print("--")
                
                
        
        
        
              