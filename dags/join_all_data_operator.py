#---Airflow libraries-----#
import datetime
import glob
import json
import os
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

#---Pandas libraries-----#
import pandas as pd


class JoinAllData(BaseOperator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
        
    def execute(self, context):
        print('Joining all data')
        self.joinScopusData()
        
    
    def joinScopusData(self):
        core_file = f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/core_data.csv"
        coredata = pd.read_csv(core_file)
        
        
        current_affiliton_file = f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/current_afilliations.csv"
        affiliation_current = pd.read_csv(current_affiliton_file)
        
        join_df = pd.merge(coredata,affiliation_current, how="left", left_on='Scopus_id', right_on='Scopus_id')
        
        print("Data joined")
        
        join_df.to_csv(f"{self.dag_path}/data/scopus/to_upload_data/authors_join.csv",index=False)
        
        
        
        
    