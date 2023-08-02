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
        #self.export_scopus_data()
        #self.export_authors_core_data()
        #self.exporting_authors_products_data()
        
    
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
            write_disposition="WRITE_TRUNCATE" 
        else:
            folder_path = f"{self.dag_path}/data/to_upload/append"    
            #write_disposition="WRITE_APPEND"
            write_disposition="WRITE_TRUNCATE" 
        
        file_paths = glob.glob(os.path.join(folder_path, '*'))
        for file_path in file_paths:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            print(f"📝File name: {file_name}, File Path: ${file_path}")
            df = pd.read_csv(file_path,low_memory=False)
            try:
                self.createTable(file_name,df,None,write_disposition=write_disposition)
            except:
                print("--")
                
                
                
    
    
           
        
    def export_scopus_data(self):
        
        folder_path = f"{self.dag_path}/data/scopus/to_upload_data"

        file_paths = glob.glob(os.path.join(folder_path, '*'))

        for file_path in file_paths:
            print(file_path)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            df = pd.read_csv(file_path)
            try:
                self.createTable(file_name,df,None)
            except:
                print("--")
                
        
    def export_authors_core_data(self):
        
        file_path = f"{self.dag_path}/data/scopus/to_upload_data/core_data.csv"

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        df = pd.read_csv(file_path)
        
        self.createTable(file_name,df,None)
        
        
        

        # for file_path in file_paths:
        #     print(file_path)
        #     file_name = os.path.splitext(os.path.basename(file_path))[0]
        #     df = pd.read_csv(file_path)
        #     try:
        #         self.createTable(file_name,df)
        #     except:
        #         print("--")        
        
        
        
        
        # file = f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/core_data.csv"
        # file_name = os.path.splitext(os.path.basename(file))[0]
        # df = pd.read_csv(file)
        # print(df.dtypes)
        # # schema=[
        # # bigquery.SchemaField("Scopus_id","INTEGER", mode="REQUIRED"),
        # # bigquery.SchemaField("orcid", "STRING", mode="NULLABLE"),
        # # bigquery.SchemaField("document_count", bigquery.enums.SqlTypeNames.INT64),
        # # bigquery.SchemaField("cited_by_count", bigquery.enums.SqlTypeNames.INT64),
        # # bigquery.SchemaField("citation_count", bigquery.enums.SqlTypeNames.INT64),
        # # bigquery.SchemaField("pick_date", "TIMESTAMP", mode="REQUIRED")
        # # ]
        # self.createTable(file_name,df)
        
        
        # file = f"{self.dag_path}/data/scopus/join_data/authors_join.csv"
        # file_name = os.path.splitext(os.path.basename(file))[0]
        # df = pd.read_csv(file)
        # print(df.dtypes)
        # # schema=[
        # # bigquery.SchemaField("Scopus_id","INTEGER", mode="REQUIRED"),
        # # bigquery.SchemaField("orcid", "STRING", mode="NULLABLE"),
        # # bigquery.SchemaField("document_count", bigquery.enums.SqlTypeNames.INT64),
        # # bigquery.SchemaField("cited_by_count", bigquery.enums.SqlTypeNames.INT64),
        # # bigquery.SchemaField("citation_count", bigquery.enums.SqlTypeNames.INT64),
        # # bigquery.SchemaField("pick_date", "TIMESTAMP", mode="REQUIRED")
        # # ]
        # self.createTable(file_name,df)
        
        
        
            
    # def exporting_authors_core_data(self):
    #     folder_path = f"{self.dag_path}/data/scopus/clean/clean_authors_core_data"

    #     # use glob to get all file paths in folder
    #     file_paths = glob.glob(os.path.join(folder_path, '*'))


    #     for file_path in file_paths:
    #         print(file_path)
    #         file_name = os.path.splitext(os.path.basename(file_path))[0]
    #         df = pd.read_csv(file_path)
    #         try:
    #             self.createTable(file_name,df)
    #         except:
    #             print("--")
            
                
    # def exporting_authors_products_data(self):
    #     folder_path = f"{self.dag_path}/data/scopus/clean/clean_authors_products_data"
    #     # use glob to get all file paths in folder
    #     file_paths = glob.glob(os.path.join(folder_path, '*'))
    #     for file_path in file_paths:
    #         print(file_path)
    #         file_name = os.path.splitext(os.path.basename(file_path))[0]
    #         df = pd.read_csv(file_path)
    #         try:
    #             self.createTable(file_name,df)
    #         except:
    #             print("--")
              