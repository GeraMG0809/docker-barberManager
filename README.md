# ✂️ BarberManager

**BarberManager** es una aplicación web diseñada para la gestión integral de una barbería. Permite administrar citas, servicios, barberos, usuarios, productos, ventas y comentarios de manera eficiente. Desarrollada con **Flask**, **MySQL** y contenida mediante **Docker**, esta herramienta es ideal para barberos o negocios que desean llevar un control digital de sus operaciones.

---

## 🚀 Tecnologías utilizadas

- Python 3.x
- Flask
- MySQL 5.7
- Docker y Docker Compose
- HTML + CSS (Bootstrap) + JavaScript

---

## 📁 Estructura del proyecto

docker-barberManager/
│
├── app/
│ ├── main.py # Archivo principal de ejecución
│ ├── models/ # Modelos y clases ORM
│ ├── helpers/ # Funciones auxiliares
│ ├── static/ # Archivos estáticos (CSS, JS, imágenes)
│ └── templates/ # Vistas HTML (Jinja2)
│
├── sql/
│ └── backup-barberManager.sql # Script SQL de respaldo para la base de datos
│
├── Dockerfile # Imagen de la app Flask
├── docker-compose.yml # Orquestador de servicios
└── README.md # Este archivo

---

## ⚙️ Instalación con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/GeraMG0809/docker-barberManager.git
cd docker-barberManager
2. Asegúrate de tener el respaldo de la base de datos
Copia el archivo backup-barberManager.sql al directorio ./sql/.

3. Construir e iniciar los servicios
sudo docker-compose up --build
Esto levantará dos contenedores:

barber_manager_app: ejecuta la aplicación Flask.

barber_manager_db: instancia de MySQL 5.7 con el respaldo cargado.

El puerto por defecto de la aplicación es 5050.

4. Accede a la aplicación
Abre tu navegador y visita:
http://localhost:5050
🧪 Base de datos
El contenedor barber_manager_db utiliza MySQL 5.7 por compatibilidad con las colaciones y definiciones del respaldo.

El respaldo backup-barberManager.sql debe contener las tablas necesarias y datos iniciales.

El nombre de la base de datos dentro del contenedor es: barber_manager_db.

📤 Importar el respaldo manualmente (opcional)
En caso de que necesites importar el respaldo manualmente:

# Copia el archivo al contenedor
docker cp sql/backup-barberManager.sql barber_manager_db:/backup-barberManager.sql

# Ingresa al contenedor MySQL
docker exec -it barber_manager_db mysql -u root -p

# Dentro del monitor de MySQL:
USE barber_manager_db;
SOURCE /backup-barberManager.sql;
🧑 Autor
Desarrollado por GeraMG0809
