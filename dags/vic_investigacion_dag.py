from airflow import DAG
from datetime import datetime


#---Operators libraries-----#

from read_scopus_operator import ReadScopus
from read_wos_operator import ReadWOS
from read_cv_lac_operator import ReadCvLAC
from read_group_lac_operator import ReadGroupLAC

from prepare_scopus_data_operator import PrepareScopusData
from prepare_wos_data_operator import PrepareWosData
from prepare_cv_lac_data_operator import PrepareCvLacData
from prepare_group_lac_data_operator import PrepareGroupLacData

from export_data_operator import ExportData
from join_all_data_operator import JoinAllData

       
                  
with DAG(
    dag_id='vic_investigacion_ETL',
    description='DAG de la vicerrectoría de investigación de la Pontificia Universidad Javeriana',
    schedule_interval='@once',
    start_date= datetime(2023, 4, 14)
    ) as dag:
    
    
    #########---------------------SCOPUS-------------------------#########
    
    read_scopus = ReadScopus(
        task_id="get_scopus_data",
        API_KEY="ecfa002fa03d10079a37957428838986"
    )
    
    prepare_scopus = PrepareScopusData(
        task_id = 'prepare_scopus_data',
    )
    
    
    # # #########---------------------------------------------------#########
    
    
    
    
        
           
    # # #########---------------------WOS---------------------------#########
               
    # # read_wos = ReadWOS(
    # #     task_id = 'get_wos_data',
    # # )
    
    # # prepare_wos = PrepareWosData(
    # #     task_id = 'prepare_wos_data',
    # # )
    
    # # #########---------------------------------------------------#########
    
    
    
    
    
    
    
    # # #########---------------------CV_LAC---------------------------#########
    
    # # read_cv_lac = ReadCvLAC(
    # # task_id = 'get_cv_lac_data',    
    # # )
    
    # # prepare_cv_lac = PrepareCvLacData(
    # #     task_id = 'prepare_cv_lac_data',
    # # )
    
    # # #########---------------------------------------------------#########
    
    
    
    
    
    
    
    
    # # #########---------------------GROUP_LAC---------------------------#########
    
    # # read_group_lac = ReadGroupLAC(
    # #     task_id = 'get_group_lac_data',
    # # )
    
        
    # # prepare_group_lac = PrepareGroupLacData(
    # #     task_id = 'prepare_group_lac_data',
    # # )
    
    # # #########---------------------------------------------------#########
    
    
    
    
    
    
    
    
    # # #########---------------------JOIN---------------------------########
    
    # # join = JoinAllData(
    # #     task_id = 'join_all_data',
    # # )
    
    # # #########---------------------------------------------------#########
    
    
    
    
    
    
    
    
           
    
    #########---------------------EXPORTING---------------------------########
    
    exporting = ExportData(
        task_id = 'upload_data_big_query',
    )
    
    #########---------------------------------------------------#########
    

    
    
    read_scopus >> prepare_scopus >> exporting
    
    # read_scopus >> prepare_scopus >> exporting
    
    
    

   #[prepare_scopus,prepare_wos,prepare_cv_lac,prepare_group_lac] >> join >> exporting
    
    
    
    
    
    



