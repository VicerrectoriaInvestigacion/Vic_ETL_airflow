# ETL Vicerrectoría de investigación

(Este proyecto es de uso exclusivo por parte de la vicerrectoría de investigación de la Pontificia Universidad Javeriana)
(Todos los derechos estás reservados por parte de la vicerrectoría de investigación de la Pontificia Universidad Javeriana)

Este proyecto consta de un DAG (Gráfico Acíclico Dirigido) desarrollado con Apache Airflow, la arquitectura de alto nivel se puede obsevar a continuación.

<img width="951" alt="Screenshot 2023-06-28 at 10 42 01 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/552d2e53-685c-4aba-bbe7-e37e4f89750b">

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

# Agregar una nueva librería

Para agregar una nueva librería para que sea instalada por pip solo se debe agregar en el campo de **_PIP_ADDITIONAL_REQUIREMENTS** en el docker-compose.yaml

<img width="734" alt="Screenshot 2023-06-26 at 6 06 28 AM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/3d86fedc-98b3-4724-b48e-2dac160c66d0">

# Crear un Operator
<img width="443" alt="Screenshot 2023-08-01 at 8 51 34 PM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/1dcf03cd-299e-4c43-98ea-85ac74f8562c">

Hacer click derecho sobre la carpeta de "dags" y crear un nuevo archivo, por conveción cada operator debe terminar con la palabra operator.
ej. cargar-info-operator.py



<img width="548" alt="Screenshot 2023-08-01 at 8 53 09 PM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/b0f85512-cdeb-4029-a549-41e1ec2a9447">

Un operator siempre tendra esta estructura, donde hereda de BaseOperator, tiene su constructor y un método "exceute" (Acá se debe llamar al código que se quiere ejecutar).

**Nota**
Siempre el constructor del Operator agregar la siguiente línea de código, esto le permitirá al DAG reconocer dónde están los datos en caso tal se quiera leer o escribir.
```sh
self.dag_path=os.getcwd()
```
Dado lo anterior, siempre se accederán a los datos mediante un path inicial: "self.dag_path/data/[PATH DEL ARCHIVO]"



# Agregar un Operator al DAG

1) Dirigirse al archivo de "vic_investigacion_dag.py" y ubicarse al final del archivo.
2) Crear una instancia de la clase del Operator creado y asignarle un "task_id" (Esto indentificará al operator).

<img width="723" alt="Screenshot 2023-08-01 at 8 55 58 PM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/8f333a96-1f2c-4f21-91f4-411e2e81b25b">


3) Creada la instancia agregarla al DAG, por lo cual:
  - Si se quiere que el Operator se corra en simultanea que los demás añadirlo dentro de los  []

<img width="1123" alt="Screenshot 2023-08-01 at 8 55 36 PM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/cc2c5eb8-63a2-42d2-9ebf-f0e2a383e7d7">


Si se quiere ejecutar uno primero que el otro acomodarlo de la siguiente manera:

<img width="458" alt="Screenshot 2023-08-01 at 9 02 07 PM" src="https://github.com/VicerrectoriaInvestigacion/Vic_ETL_airflow/assets/52805660/51a3873d-94ea-454f-8e2e-67b4ffc4bf0a">



