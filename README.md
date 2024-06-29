# Sistema de Inscripción Universitaria

Este proyecto permite la gestión de inscripciones de estudiantes a diversas carreras universitarias utilizando SQLAlchemy para manejar la base de datos. Los datos de los estudiantes se almacenan en una base de datos SQLite.



## Funcionalidades

**Inscripción de estudiantes:** Registra nuevos estudiantes con su nombre, apellido, matrícula y DNI.

**Gestión de carreras:** Permite la creación y consulta de carreras universitarias.

**Inscripción a carreras:** Asigna estudiantes a carreras específicas.

**Exportación a CSV:** Genera un archivo CSV con los datos de los estudiantes y sus carreras.



## Estructura del Proyecto

`database.py`: Configuración de la base de datos y creación de la sesión.

`crud.py`: Operaciones CRUD para manejar estudiantes y carreras.

`main.py`: Punto de entrada del programa, con la lógica de interacción del usuario y exportación de datos.

`modelo.py`: Definición de las clases de modelo para estudiantes y carreras.



## Instalación

1. Clona este repositorio.
   ```bash
   git clone https://github.com/nahuquiroga/Equipo-7-SQLAlchemy.git
   ```
   
2. Instala las dependencias.
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el script principal.
   ```bash
   python main.py
   ```
   
2. Sigue las instrucciones en pantalla para inscribir estudiantes y gestionar sus inscripciones.
   


## Exportación de Datos
Después de finalizar las operaciones, los datos de los estudiantes se exportarán automáticamente a un archivo students_sorted.csv.

