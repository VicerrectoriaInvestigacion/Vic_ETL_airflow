from airflow import DAG
from datetime import datetime

#---Operators-----#

from read_scopus_operator import ReadScopus
from read_wos_operator import ReadWOS
from read_cv_lac_operator import ReadCvLAC
from read_group_lac_operator import ReadGroupLAC

from prepare_revistas_operator import PrepareRevistas
from prepare_profesores_validado_operator import PrepareProfesoresValidados
from prepare_produccion_validada_operator import PrepareProduccionValidada
from prepare_profesores_data_operator import PrepareProfesoresData
from prepare_semilleros_operator import PrepareSemilleros
from prepare_proyectos_operator import PrepareProyectos


from prepare_scopus_data_operator import PrepareScopusData
from prepare_wos_data_operator import PrepareWosData
from prepare_cv_lac_data_operator import PrepareCvLacData
from prepare_group_lac_data_operator import PrepareGroupLacData
from prepare_repositorio_inst_operator import PrepareRepositorioInstitucional


from export_data_operator import ExportData
from join_all_data_operator import JoinAllData

       
                  
with DAG(
    dag_id='vic_investigacion_ETL',
    description='DAG de la vicerrectoría de investigación de la Pontificia Universidad Javeriana',
    schedule_interval='@once',
    start_date= datetime.now()
    ) as dag:
    
    
    ########---------------------SCOPUS-------------------------#########
    
    # read_scopus = ReadScopus(
    #     task_id="get_scopus_data",
    #     API_KEY="ecfa002fa03d10079a37957428838986"
    # )
    
    # prepare_scopus = PrepareScopusData(
    #     task_id = 'prepare_scopus_data',
    # )
    
    
    # # # #########---------------------------------------------------#########
    
    
    
    
        
           
    # #########---------------------WOS---------------------------#########
               
    # read_wos = ReadWOS(
    #     task_id = 'get_wos_data',
    # )
    
    # prepare_wos = PrepareWosData(
    #     task_id = 'prepare_wos_data',
    # )
    
    # #########---------------------------------------------------#########
    
    
    
    
    
    
    
    # #########---------------------CV_LAC---------------------------#########
    
    # read_cv_lac = ReadCvLAC(
    # task_id = 'get_cv_lac_data',    
    # )
    
    # prepare_cv_lac = PrepareCvLacData(
    #     task_id = 'prepare_cv_lac_data',
    # )
    
    # #########---------------------------------------------------#########
    
    
    
    
    
    
    
    
    # #########---------------------GROUP_LAC---------------------------#########
    
    # read_group_lac = ReadGroupLAC(
    #     task_id = 'get_group_lac_data',
    # )
    
        
    # prepare_group_lac = PrepareGroupLacData(
    #     task_id = 'prepare_group_lac_data',
    # )
    
    # #########---------------------------------------------------#########
    
            
    
    # #########---------------------PROFESORES VALIDADOS---------------------------########
    
    profesores_validados = PrepareProfesoresValidados(
        task_id = 'profesores_validados',
    )
    
    # #########---------------------------------------------------#########
    
    
    ##########---------------------PROFESORES CORE DATA---------------------------########
    
    profesores_core_data = PrepareProfesoresData(
        task_id = 'profesores_core_data',
    )
    
    # #########---------------------------------------------------#########
    
    
    
    
    # #########---------------------PRODUCCIÓN VALIDADA---------------------------########
    
    produccion_validada = PrepareProduccionValidada(
        task_id = 'produccion_validada',
    )
    
    # #########---------------------------------------------------#########
    
    
       
    #########---------------------JOURNALS---------------------------#########

    revistas = PrepareRevistas(
        task_id = 'revistas',
    )


    #########---------------------------------------------------#########
    
    
    #########---------------------SEMILLEROS---------------------------#########

    semilleros = PrepareSemilleros(
        task_id = 'semilleros',
    )


    #########---------------------------------------------------#########
    
    
    #########---------------------SEMILLEROS---------------------------#########

    proyectos = PrepareProyectos(
        task_id = 'proyectos',
    )

    #########---------------------------------------------------#########
    
    
    
    
    
    #########---------------------REPOSITORIO_INSTITUCIONAL---------------------------#########


    repositorio_inst = PrepareRepositorioInstitucional(
        task_id = 'repositorio_institucional',
    )
    
    #########---------------------------------------------------#########
    
    
    
    
    # #########---------------------JOIN---------------------------########
    
    # join = JoinAllData(
    #     task_id = 'join_all_data',
    # )
    
    # #########---------------------------------------------------#########
    
           
    
    #########---------------------EXPORTING---------------------------########
    
    exporting = ExportData(
        task_id = 'upload_data_big_query',
    )
    
    #########---------------------------------------------------#########
    

    
    profesores_validados >>  profesores_core_data
    
    
    profesores_core_data >> exporting
    
    
    
    [profesores_validados,profesores_core_data,produccion_validada,revistas,semilleros,proyectos,repositorio_inst] >> exporting
    
    
   #read_journals >> produccion_validada  >> profesores_validados >> exporting
    
    #read_scopus >> prepare_scopus >> exporting
    
    #read_repositorio_inst >> prepare_repositorio_inst >> exporting

    # read_scopus >> prepare_scopus

    # read_wos >> prepare_wos

    # read_cv_lac>>prepare_cv_lac

    # read_group_lac >> prepare_group_lac
    
    # read_repositorio_inst >> prepare_repositorio_inst
    
    # [prepare_scopus,prepare_wos,prepare_cv_lac,prepare_group_lac,prepare_repositorio_inst,read_journals] >> join >> exporting
    

    #read_journals >> exporting

    
    
    
    
    
    



