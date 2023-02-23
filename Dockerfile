FROM apache/airflow:2.5.1

USER airflow

RUN pip install scrapy

#RUN pip install -r requirements.txt
