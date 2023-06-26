# ETL Vicerrectoría de investigación

(Este proyecto es de uso exclusivo por parte de la vicerrectoría de investigación de la Pontificia Universidad Javeriana)
(Todos los derechos estás reservados por parte de la vicerrectoría de investigación de la Pontificia Universidad Javeriana)

Este proyecto consta de un DAG (Gráfico Acíclico Dirigido) desarrollado con Apache Airflow, la arquitectura de alto nivel se puede obsevar a continuación.

<img width="1535" alt="Screenshot 2023-06-26 at 5 42 16 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/b086279b-65f3-476a-bb00-4071c4a3e74f">


# Correr el proyecto

Para correr el DAG primero es necesario correr el archivo docker-compose, para ello se debe ubiscar desde la terminal la ruta donde se tiene el proyecto , después se debe correr alguno de los siguientes comandos desde la terminal:


Para correr el proyecto de Apache Airflow
```sh
docker-compose up
```

Para correr el proyecto de Apache Airflow y tener en cuenta cambios realizados en el archivo docker-compose.yaml (Esto solo se corre si se hicieron cambios en docker-compose.yaml)
```sh
docker-compose up --build
```


Para parar los contenedores (En general todo el proyecto):

```sh
docker-compose stop
```


Para parar los contenedores (En general todo el proyecto) y eliminar los contenedores:

```sh
docker-compose down
```







