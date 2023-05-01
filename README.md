# Departamento de Ingeniería de Sistemas y Computación
# ISIS 3301 – Inteligencia de  Negocios
## Proyecto Analítica de textos 

|Integrantes|Código|Correo|
|----|----|----|
|Julian Andres Mendez Melo|201920623|j.mendezm@uniandes.edu.co|
|María Alejandra Vargas Torres|201123148|ma.vargas73@uniandes.edu.co|
|Omar Esteban Vargas Salamanca|201921271|o.vargas@uniandes.edu.co|

#### Caso de estudio 
- [Cronograma y organización](https://github.com/users/Uniandes-byte/projects/1): Cada integrante tiene asignadas las tareas junto con los tiempos de la misma. 
#### Parte 1

##### Repositorio
- [Wiki](https://github.com/Uniandes-byte/ProyectoUno/wiki): Organización del grupo, las actas de reunión y entregables para la etapa 1. 

##### Contenido
1. En la carpeta *Datos* se encuentran los de prueba y los que se utilizaron para el entrenamiento. 
2. El archivo Proyecto_Parte_1.ipynb es el que contiene el jupyter ejecutado con los datos del proyecto. 
3. El documento Proyecto_Parte_1.pdf tiene la documentación y el proceso realizado.

#### Parte 2

##### Repositorio
- [Wiki](https://github.com/Uniandes-byte/ProyectoUno/wiki/Proyecto-1---Parte-2): Organización del grupo, las actas de reunión y entregables para la etapa 1. 

##### Pasos para ejecutar el proyecto  
1. Crear una carpeta llamada `Bisness Intelligence`
2. Clonar el repositorio dentro de la carpeta con el siguiente comando:

```
git clone https://github.com/Uniandes-byte/ProyectoUno.git
```

3. Crear un ambiente virtual al mismo nivel de la carpeta generada cuando se clono el repositorio. Para ello, ejecute el siguiente comando:

```
python -m venv venv
```

4. Instalar las dependencias del proyecto en el ambiente virtual. Para ello, primero abra visual studio code, ubiquese en la termina cmd y dirigase a la siguiente ruta: 

```
ProyectoUno\Parte 2\text_analytics>
```

5. Instale las dependecias del archivo requirements por medio del siguiente comando:

```
pip install -r requirements.txt
```

6. En este paso ya tendrá configurado el proyecto de django. 

7. Ahora es necesario crear la base de datos `MySql`. Es importante tener en cuenta que el usuario admin debe llamarse `root` y la contraseña debe ser `admin`. De no ser así, debe entrar en el archivo `text_analytics\settings.py` y cambiar el parámetros `USER` (línea 97) por el nombre de usuario escogido y el parámetros `PASSWORD` (línea 98) por la contraseña escogida. Luego cree una base de datos llamada  `text_analytics`. Todos estos pasos los puede encontrar en el siguiente tutorial: 

https://medium.com/@a01207543/django-conecta-tu-proyecto-con-la-base-de-datos-mysql-2d329c73192a

8. Realiza las migraciones de las aplicaciones de Django con el siguiente comando:

```
python manage.py makemigrations
```

9. Mandar las migraciones a la base de datos con el siguiente comando:

```
python manage.py migrate
```

10. Ejecutar el proyecto

```
python manage.py runserver
```

11. Automáticamente la aplicación se desplegara en el localhost en la url:

http://127.0.0.1:8000/inicio

12. Ahora podra navegar por la aplicación de forma libre por medio de la barra de navegación y, así mismo, podrá probarla. Recuerde que para dejar de desplegar la aplicación deberá oprimir ctrl+c en el terminal donde se encuentra ejecutandola.



