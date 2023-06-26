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


class ReadScopus(BaseOperator):

    def __init__(self, API_KEY, **kwargs):
        super().__init__(**kwargs)
        self.API_KEY = API_KEY
        self.scopus_client = ElsClient(self.API_KEY)
        self.dag_path=os.getcwd()
        
    def execute(self, context):
        print('Getting Scopus Data')
        print("The api key is: ", self.API_KEY)
        self.saveData()
        
    def saveData(self):
        
        print("DAG PATH: ",self.dag_path)
        authors_ids_data= pd.read_excel(f"{self.dag_path}/data/authors_ids/authors_ids.xlsx")
        authors_ids_data=authors_ids_data.loc[authors_ids_data["Scopus_ID"].notna()]
        authors_ids_data["Cedula"] = authors_ids_data["Cedula"].fillna(-1).astype(int).astype(str)
        authors_ids_data["Scopus_ID"] = authors_ids_data["Scopus_ID"].astype(int).astype(str)
        
        authors_data=[]
        authors_products_data=[]
        
        for index, row in authors_ids_data.iterrows():                  
            authors_data.append(self.getAuthorData(author_id=row["Scopus_ID"],author_name=row["Nombre"],client=self.scopus_client))
            authors_products_data.extend(self.getAuthorProducts(author_id=row["Scopus_ID"],author_name=row["Nombre"],client=self.scopus_client))

        
        self.save_data_dfs(authors_list_data=authors_data,authors_list_products_data=authors_products_data)
       
    def save_data_dfs(self,authors_list_data,authors_list_products_data):
        authors_data_df = pd.DataFrame(authors_list_data)  
        authors_data_df.to_csv(f"{self.dag_path}/data/scopus/raw/authors_raw_data/authors_data_raw.csv",index=False) 
           
        authors_products_data_df = pd.DataFrame(authors_list_products_data)  
        authors_products_data_df.to_csv(f"{self.dag_path}/data/scopus/raw/authors_raw_products_data/authors_raw_products_data.csv",index=False)    
                  
    def getAuthorData(self,author_id,author_name,client):
        
        # Initialize author with uri
        my_auth = ElsAuthor(
            uri = f'https://api.elsevier.com/content/author/author_id/{author_id}')

        if my_auth.read(client):
            data = my_auth.data
            del data["@status"]
            del data["@_fa"]
            json_object = json.dumps(data)
            data = json.loads(json_object)
            data["Scopus_ID"]=author_id
            data["Author_name"]=author_name
            print(data)
            return data

    def getAuthorProducts(self,author_id,author_name,client):
        print(author_id)
        # Initialize author products with Author ID
        auth_products = ElsSearch("AU-ID({})".format(author_id), "scopus")
        auth_products.execute(client)
        json_object = json.dumps(auth_products.results)
        data = json.loads(json_object)
        products=[]
        for product in data:
            del product["link"]
            del product["@_fa"]
            del product["prism:url"]
            product["Scopus_ID"]=author_id
            product["Author_name"]=author_name
            
            if "affiliation" in product:
                containsJaverianaAffil=False
                for affs in product["affiliation"]:
                    print(affs["affilname"])
                    if "javeriana" in str(affs["affilname"]).lower() or "hospital universitario san ignacio" in str(affs["affilname"]).lower():
                        containsJaverianaAffil=True  
                print("-------------------------------------")        
                if containsJaverianaAffil:
                    products.append(product)
                
            # if 'prism:isbn' in product:
            #     isbns = product.get('prism:isbn', [])
            #     product.update({f"isbn_{index+1}": str('{:.0f}'.format(int(isbn['$']))) for index, isbn in enumerate(isbns)})   
            
        # print("*****************************************")
        return products
