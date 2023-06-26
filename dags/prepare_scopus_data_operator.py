#---Airflow libraries-----#
import datetime
import glob
import json
import os
import re
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import numpy as np
#---Pandas libraries-----#
import pandas as pd


class PrepareScopusData(BaseOperator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dag_path=os.getcwd()
        
    def execute(self, context):
        print('Preparing Scopus Data')
        
        self.prepare_authors_data()
        
        # self.clean_authors_core_data()
        # self.clean_authors_products_data()
        
        
    def _parse_json(self,x):
        try:
            return json.loads(x)
        except (json.JSONDecodeError, TypeError):
            print("Error data: ",x)
            x=x.replace("@", "_")
            print("After replace: ",x)
            try:
                return json.loads(x)
            except (json.JSONDecodeError, TypeError):
                return "Error-Verificar"   
   
    def saveData(self,coredata,subject_areas_dataframe, products_df):
       coredata.to_csv(f"{self.dag_path}/data/scopus/to_upload_data/core_data.csv",index=False)
       subject_areas_dataframe.to_csv(f"{self.dag_path}/data/scopus/to_upload_data/subject_areas.csv",index=False)
       products_df.to_csv(f"{self.dag_path}/data/scopus/to_upload_data/products.csv",index=False)
       
       #subject_areas_dataframe.to_csv(f"{self.dag_path}/data/scopus/to_upload_data/subject_areas.csv",index=False)   
       #subject_areas_dataframe.to_csv(f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/subject_areas.csv",index=False)
       
   
    def cleanCoreData(self,coredata,main_df):
        coredata=pd.json_normalize(coredata)
        coredata.drop(columns=["prism:url","link","eid"],inplace=True)
        coredata["dc:identifier"]=coredata["dc:identifier"].str.replace("AUTHOR_ID:","")
        coredata=coredata.rename(columns={"dc:identifier":"Scopus_ID",
                                          "document-count":"document_count",
                                          "cited-by-count":"cited_by_count",
                                          "citation-count":"citation_count"})
        coredata["Author_name"]=main_df["Author_name"]
        coredata["pick_date"] = datetime.datetime.now()
        return coredata
    
    
    def cleanProductsData(self,products):
        pr_columns=products.columns
        formatted_pr_columns = [str(col).replace("-", "_") for col in pr_columns]
        formatted_pr_columns = [str(col).replace("dc:", "") for col in formatted_pr_columns]
        formatted_pr_columns = [str(col).replace("prism:", "") for col in formatted_pr_columns]
        rename_columns= dict(zip(pr_columns, formatted_pr_columns))
        products_df=products.rename(columns=rename_columns)
        products_df["identifier"]=products_df["identifier"].str.replace("SCOPUS_ID:","")
        products_df["pick_date"] = datetime.datetime.now()
        return products_df
    
     
    def cleanSubjectsData(self,subject_areas,main_df):
        subject_areas=pd.json_normalize(subject_areas)
        columns_sub = ['@_fa', '@abbrev', '@code', '$','Scopus_ID']
        subject_areas_dataframe = pd.DataFrame(columns=columns_sub)

        for index,subject in enumerate(subject_areas["subject-area"]):
            norm_sub=pd.json_normalize(subject)
            norm_sub["Scopus_ID"]=main_df["Scopus_ID"][index]
            norm_sub["Author_name"]=main_df["Author_name"][index]
            dta=pd.DataFrame(norm_sub)
            subject_areas_dataframe = pd.concat([subject_areas_dataframe,dta])
        
        subject_areas_dataframe=subject_areas_dataframe.rename(columns={"$":"Subject_area","@code":"Codigo","@abbrev":"abbrev"})
        subject_areas_dataframe.drop(columns=["@_fa"],inplace=True)
        
        return  subject_areas_dataframe  
   
    def prepare_authors_data(self):
        df=pd.read_csv(f"{self.dag_path}/data/scopus/raw/authors_raw_data/authors_data_raw.csv")
        
        for column in df.columns[:-2]:
            df[column] = df[column].apply(lambda x:  re.sub(r"(?<!:|\w)d'", '°', x)  if pd.notnull(x) else np.nan)
            df[column] = df[column].apply(lambda x: x.replace("'", "\"") if pd.notnull(x) else np.nan)
            print("Column:", column)
            df[column] = df[column].apply(lambda x: np.nan if pd.isnull(x) else self._parse_json(x))
        
        
        
        coredata= self.cleanCoreData(df["coredata"],main_df=df)
        subject_areas_dataframe= self.cleanSubjectsData(df["subject-areas"], main_df=df)
        
        
        df_products=pd.read_csv(f"{self.dag_path}/data/scopus/raw/authors_raw_products_data/authors_raw_products_data.csv")
        
        clean_products= self.cleanProductsData(df_products)
        
        self.saveData(coredata,subject_areas_dataframe,clean_products)
        
        
            
    
    
    
    
        
    # def clean_authors_core_data(self):
    #     folder_path = f"{self.dag_path}/data/scopus/raw/authors_raw_data"

    #     # use glob to get all file paths in folder
    #     file_paths = glob.glob(os.path.join(folder_path, '*'))

    #     # iterate over file paths and read each file
    #     core_data_dataframe= pd.DataFrame()
    #     currentAfilliton_dataframe= pd.DataFrame()
    #     afilliton_history_dataframe= pd.DataFrame()
    #     subject_areas_dataframe= pd.DataFrame()

    #     for file_path in file_paths:
    #         with open(file_path, 'r') as file:
    #             json_data = json.load(file)
    #             coredata = pd.json_normalize(json_data["coredata"])
    #             coredata.drop(columns=["link","eid","prism:url"],inplace=True)
    #             coredata.rename(columns = {"dc:identifier":"Scopus_id",
    #                                        "document-count":"document_count",
    #                                        "cited-by-count":"cited_by_count",
    #                                        "citation-count":"citation_count"
    #                                        },inplace=True)
    #             coredata["Scopus_id"]=coredata["Scopus_id"].str[10:]
    #             coredata["pick_date"]=datetime.datetime.now()
    #             core_data_dataframe = pd.concat([core_data_dataframe,coredata])
                
                
                
    #             affiliation_current=df = pd.json_normalize(json_data["author-profile"])
    #             affiliation_current = affiliation_current.loc[:, affiliation_current.columns.str.contains('affiliation-current|status')]
                
                
    #             affiliation_current = affiliation_current.rename(columns=lambda x: x.replace('-', '_'))
                
    #             affiliation_current.drop(columns=["affiliation_current.affiliation.ip_doc.@id",
    #                               "affiliation_current.affiliation.ip_doc.@type",
    #                               "affiliation_current.affiliation.ip_doc.afnameid",
    #                               "affiliation_current.affiliation.ip_doc.manual_curation.@curated",
    #                               "affiliation_current.affiliation.ip_doc.manual_curation.curation_type",
    #                               "affiliation_current.affiliation.ip_doc.preferred_name.$",
    #                               "affiliation_current.affiliation.ip_doc.sort_name",
    #                               "affiliation_current.affiliation.ip_doc.address.address_part",
    #                               "affiliation_current.affiliation.ip_doc.address.@country",
    #                               "affiliation_current.affiliation.ip_doc.org_domain",
    #                               "affiliation_current.affiliation.ip_doc.org_URL",
    #                               "affiliation_current.affiliation.@source",
    #                               "affiliation_current.affiliation.ip_doc.preferred_name.@source",
    #                               "affiliation_current.affiliation.ip_doc.manual_curation.curation_source"
    #                               ],inplace=True)
               
                
    #             affiliation_current = affiliation_current.rename(columns=lambda x: "Current_affil_" + x.split('@')[-1].split('.')[-1])
                
    #             affiliation_current["Scopus_id"]= coredata["Scopus_id"]
                
    #             currentAfilliton_dataframe = pd.concat([currentAfilliton_dataframe,affiliation_current])


    #             affiliation_history=pd.json_normalize(json_data["author-profile"]["affiliation-history"],record_path=["affiliation"])
    #             affiliation_history["Author_scopus_id"]= coredata["Scopus_id"][0]
    #             afilliton_history_dataframe=pd.concat([afilliton_history_dataframe,affiliation_history])


    #             subject_areas=pd.json_normalize(json_data["subject-areas"]["subject-area"])
    #             subject_areas["Scopus_id"]= coredata["Scopus_id"][0]
    #             subject_areas.drop(columns=["@_fa"],inplace=True)
    #             subject_areas.rename(columns={"@abbrev":"abbrev","$":"area","@code":"code"},inplace=True)
                
                
    #             subject_areas_dataframe=pd.concat([subject_areas_dataframe,subject_areas])    
         
         
    #     core_data_dataframe.to_csv(f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/core_data.csv",index=False)
    #     currentAfilliton_dataframe.to_csv(f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/current_afilliations.csv",index=False)
    #     afilliton_history_dataframe.to_csv(f"{self.dag_path}/data/scopus/clean/clean_authors_core_data/afilliations_history.csv",index=False)
    #     subject_areas_dataframe.to_csv(f"{self.dag_path}/data/scopus/to_upload_data/subject_areas.csv",index=False)
                
    # def clean_authors_products_data(self):
        # folder_path = f"{self.dag_path}/data/scopus/raw/authors_raw_products_data"
        
        # # use glob to get all file paths in folder
        # file_paths = glob.glob(os.path.join(folder_path, '*'))

        # # iterate over file paths and read each file
        # product_dataframe= pd.DataFrame()
        # for file_path in file_paths:
        #     with open(file_path, 'r') as file:
        #         json_data = json.load(file)
        #         print(json_data)

        #         products=pd.json_normalize(json_data)
        #         isbn=products["prism:isbn"].explode().apply(pd.Series)
        #         isbn.drop(columns=["@_fa",0],inplace=True)
        #         isbn.rename(columns={"$":"isbn"},inplace=True)
        #         products.drop(columns=["prism:isbn","@_fa","link","freetoread.value","freetoreadLabel.value","prism:coverDisplayDate","openaccess","prism:aggregationType","subtype","affiliation"],inplace=True)
        #         products = pd.concat([products,isbn],axis=1)
        #         product_dataframe = pd.concat([product_dataframe,products])          
        
        # product_dataframe.to_csv(f"{self.dag_path}/data/scopus/clean/clean_authors_products_data/clean_products.csv")        