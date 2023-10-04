from airflow import DAG
from datetime import datetime

#---Operators-----#

from prepare_revistas_operator import PrepareRevistas
from prepare_profesores_validado_operator import PrepareProfesoresValidados
from prepare_produccion_validada_operator import PrepareProduccionValidada
from prepare_profesores_data_operator import PrepareProfesoresData
from prepare_semilleros_operator import PrepareSemilleros
from prepare_proyectos_operator import PrepareProyectos
from prepare_contratos_operator import PrepareContratos
from prepare_repositorio_inst_operator import PrepareRepositorioInstitucional
from export_data_operator import ExportData


       
                  
with DAG(
    dag_id='vic_investigacion_ETL',
    description='DAG de la vicerrectoría de investigación de la Pontificia Universidad Javeriana',
    schedule_interval='@once',
    start_date= datetime.now()
    ) as dag:
    
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
    
    
            
    #########---------------------CONTRATOS---------------------------#########


    contratos = PrepareContratos(
        task_id = 'contratos',
    )
    
    #########---------------------------------------------------#########
    
    
        
    #########---------------------EXPORTING---------------------------########
    
    exporting = ExportData(
        task_id = 'upload_data_big_query',
    )
    
    #########---------------------------------------------------#########
    

    
    
    [profesores_validados,profesores_core_data,produccion_validada,revistas,semilleros,proyectos,repositorio_inst,contratos] >> exporting
    
    

    
    
    
    
    
    



