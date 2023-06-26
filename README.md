# ETL Vicerrectoría de investigación

(Este proyecto es de uso exclusivo por parte de la vicerrectoría de investigación de la Pontificia Universidad Javeriana)
(Todos los derechos estás reservados por parte de la vicerrectoría de investigación de la Pontificia Universidad Javeriana)

Este proyecto consta de un DAG (Gráfico Acíclico Dirigido) desarrollado con Apache Airflow, la arquitectura de alto nivel se puede obsevar a continuación.

<img width="1535" alt="Screenshot 2023-06-26 at 5 42 16 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/b086279b-65f3-476a-bb00-4071c4a3e74f">


# Correr el proyecto

Para correr el DAG primero es necesario correr el archivo docker-compose, para ello se debe ubicar desde la terminal la ruta donde se tiene el proyecto, después, se debe correr alguno de los siguientes comandos desde la terminal:


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

Posteriormente, se debe abrir en el navegador la siguiente url:

```sh
http://localhost:8080/
```
Se observa que el proyecto se corre en el puerto 8080 en la máquina local.

Si todo corrió con éxito se debe observar la siguiente pantalla en el navegador:

<img width="640" alt="Screenshot 2023-06-26 at 6 02 09 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/9320c42c-2c37-4116-a83e-424aa6e4e99b">

para poder ingresar a la consola de Airflow, ingresar la siguientes credenciales:

| Credencial | Value |
| ------ | ------ |
| Username | airflow |
| Password | airflow |


# Agregar una nueva carpeta con datos

<img width="349" alt="Screenshot 2023-06-26 at 5 57 26 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/1ae89e58-0053-46c5-9940-c34e2650ff24">

Se debe subir todas las carpetas o archivos que contengan datos a la carpeta "data", este es un volumen que se creó con el fin de reservar un espacio para aquellos archivos que posteriormente se leerán en alguno(s) nodo(s) del DAG, a continuación se puede observar cóno está creado el volumen en el docker-compose.yaml.


<img width="767" alt="Screenshot 2023-06-26 at 6 00 00 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/5b065484-650e-4721-b311-9221eb5aa2a2">


