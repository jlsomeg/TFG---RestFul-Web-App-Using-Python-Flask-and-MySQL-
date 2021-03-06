# TFG-ELORecommender

Trabajo Fin de Grado en Ingeniería Informática, Universidad Complutense de Madrid.

## Configuracion para el despliegue (Con docker-compose)

1. Ten **Docker** (con Docker-Compose) iniciado / Have **Docker**(with Docker-Compose) running

2. Descarga los archivos del repositorio / Download the repository files

	- Si lo haces con **git clone en Windows**, ejecuta antes `git config --global core.autocrlf false` para que este no convierta finales de línea al estilo Windows \r \n en lugar de los finales de línea \n que bash espera. / If you do it with **git clone on Windows**, first run `git config --global core.autocrlf false` so that it does not convert line endings to the Windows \r \n style instead of the line endings \n that bash expects.
    
3. En la carpeta donde tengas el repositorio **ejecuta** a traves de un terminal `docker-compose up` / In the folder where you have the repository **run** through a terminal `docker-compose up`

    - En caso de querer eliminar los contenedores usa `docker-compose down --rmi all` / 
If you want to eliminate the containers use `docker-compose down --rmi all`

4. Las imagenes se crearan a partir de las instrucciones introducidas en los Dockerfiles y en el yalm Docker-Compose / The images will be created from the instructions entered in the Dockerfiles and in the yalm Docker-Compose

    - El sofwtare crea 2 imagenes, **acr-mysql** donde se alojara la bd y **acr-app** donde se alojara el servicio web
    
    - Las imagenes correran sobre la **ultima distribucion de ubuntu** usando python3, entre otras dependencias / The images will run on       the **last distribution of ubuntu** using python3, among other dependencies
    
    - Se prodra acceder a la db a traves del **puerto 3306** y al servicio web a traves del **puerto 8181** / The db can be accessed through **port 3306** and the web service through **port 8181**
    
    - Para la sincronizacion entre contenedores, se ha utilizado la herramienta [wait-for-it](https://github.com/vishnubob/wait-for-it) de @vishnubob //  For the synchronization between containers, the [wait-for-it](https://github.com/vishnubob/wait-for-it) tool of @vishnubob has been used
    
5. El script de docker-compose **lanzara los contenedores en sus respectivos puerto de manera sincronizada y se encargara de la comunicacion entre estos** / The docker-compose script will **launch the containers in their respective ports in a synchronized manner and will take care of the communication between them**

6. Podremos probar si el servicio funciona en rutas como por ejemplo `http://localhost:8181/problem_list` / We can test if the service works on routes such as `http://localhost:8181/problem_list`

Usar `docker system prune -a` para limpiar de vez en cuando / Use `docker system prune -a` to clean once in a while

## Configuracion para el despliegue (Sin Docker)

1. Cambiar los valores pymysql.connect por los de tu base de datos en localhost / Change the values pymysql.connect to those of your database in localhost

2. En mysql_test.py, cambiar app.run() por el host y el puerto donde vas a colgar el servicio / In mysql_test.py, change app.run () to the host and port where you are going to hang the service

3. Importar: Flask, flask_restful, request, pymysql, mysql.connector,flask_wtf,wtforms,plotly / Import: Flask, flask_restful, request, pymysql, mysql.connector,flask_wtf,wtforms,plotly

4. Xampp up (mysql and apache)
