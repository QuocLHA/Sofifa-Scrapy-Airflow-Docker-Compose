# Sofifa-Scrapy-Airflow-Docker-Compose
A data crawl project to get football player datasets from sofifa.com (FIFA23) into the PostgreSQL server as a Data warehouse. All tasks are scheduled on Airflow in Docker-Compose. 
Project run on Ubuntu 20.04 server.

**1. CREATE PROJECT DICRECTORY & GIT CLONE**
 * "mkdir sofifa"  
 * "cd sofifa"  
 * "git clone https://github.com/QuocLHA/Sofifa-Scrapy-Airflow-Docker-Compose.git"  
 
 
**2. RUN DOCKER-COMPOSE & AIRFLOW DAGS**
 * "docker compose up -d"  
 * Create data/json directory into dags directory
 * "chmod -R 777 path/to/project"
 * Login Airflow at "http://localhost:8080/" with user: 'airflow', pass: 'airflow'  

**3. RUN ETL PROCESS IN DAGS**
* Create connection to PostgreSQL server with 'host' is IP shown in "ifconfig docker0", database, user, passwoed are all 'airflow'  
* Run Dags in Airflow for ETL process: **Crawl -> Transform -> PostgreSQL**

**4. VISUALIZATION**  
* USE Metabase connect to PostgreSQL server refer to "https://www.digitalocean.com/community/tutorials/how-to-install-metabase-on-ubuntu-20-04-with-docker"
* Dashboard
* ![image](https://user-images.githubusercontent.com/108084669/234054549-2a6695a5-2fc2-4155-9ea3-dc14c9102a69.png)
