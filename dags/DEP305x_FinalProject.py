from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

import os.path
import os
import pandas as pd
import numpy
from datetime import datetime
import json

default_args = {
   'start_date': datetime(2020, 1, 1),
}

dirname = os.path.dirname(__file__)

def _delete_json():
   if os.path.exists(dirname + "/data/json/players_urls.json"):
      os.remove(dirname + "/data/json/players_urls.json")
   if os.path.exists(dirname + "/data/json/players_stats.json"):
      os.remove(dirname + "/data/json/players_stats.json")

def _transform():
   df = pd.read_json (dirname + '/data/json/players_stats.json',encoding='utf-8-sig')

   # cột position chứa 1 array từ scrapy, lệnh này đưa array vế string
   df.positions = ['|'.join(map(str, l)) for l in df.positions]


   # Làm gọn cột player_traits
   df.player_traits = ['|'.join(map(str, l)) for l in df.player_traits]

   # Làm gọn cột player_hashtags
   df.player_hashtags = ['|'.join(map(str, l)) for l in df.player_hashtags]
   df.player_hashtags.replace(('\xa0', ''))

   # Các cột bên dưới được đổi tên lại để đồng bộ với tên các cột khác.
   df.rename(columns = {'id':'sofifa_id','name':'long_name','birth_date':'dob','height':'height_cm','weight':'weight_kg',
                           'Overall Rating':'overall_rating', 'Potential':'potential_rating','Value':'value_euro', 'Wage':'wage_euro',
                           'Preferred Foot':'preferred_foot','Weak Foot':'weak_foot','Skill Moves':'skill_moves',
                           'International Reputation':'international_reputation','Work Rate':'work_rate','Body Type':'body_type',
                           'Real Face':'real_face','Release Clause':'release_clause_euro'},inplace = True)

   df.dob = pd.to_datetime(df.dob, format="%Y/%b/%d")
   #df.dob.dt.strftime('%Y-%m-%d')

   # Hàm xóa symbol €
   def delete_euro_symbol(df):
      df.value_euro = df.value_euro.str.replace('€', '')
      df.wage_euro = df.wage_euro.str.replace('€', '')
      df.release_clause_euro = df.release_clause_euro.str.replace('€', '')
      return df

   # Hàm dùng để biến đổi giá trị ở các cột value, wage, release_clause thành các số thực.
   def converter_str_to_float(x):
      if 'M' in x:
         return float(x.strip('M'))*1000000
      elif 'K' in x:
         return float(x.strip('K'))*1000
      else:
         return float(x)

   def converter_float_to_int(x):
      return int(x)

   # Thêm '€0' vào blank cell
   df.release_clause_euro.fillna('€0', inplace = True)

   delete_euro_symbol(df)
   df.value_euro = df.value_euro.apply(converter_str_to_float)
   df.wage_euro = df.wage_euro.apply(converter_str_to_float)
   df.release_clause_euro = df.release_clause_euro.apply(converter_str_to_float)

   df.value_euro = df.value_euro.apply(converter_float_to_int)
   df.wage_euro = df.wage_euro.apply(converter_float_to_int)
   df.release_clause_euro = df.release_clause_euro.apply(converter_float_to_int)

   df = df.drop_duplicates()

   df.to_csv (dirname + '/dbdata/players_stats.csv', encoding='utf-8-sig', index = False)

with DAG(
   "DEP305x",
   schedule_interval="@daily",
   default_args=default_args,
   catchup=False   
) as dag:

   start = DummyOperator(
      task_id="start"
   )

   transform = PythonOperator(
      task_id="transform",
      python_callable=_transform,
      do_xcom_push=False  
   )

   delete_json = PythonOperator(
      task_id="delete_json",
      python_callable=_delete_json,
      do_xcom_push=False  
   )

   create_table = PostgresOperator(
      sql="sql/create_table.sql",
      task_id="create_table", 
      postgres_conn_id="postgres_local",
      dag=dag
   )

   drop_table = PostgresOperator(
      sql="sql/drop_table.sql",
      task_id="drop_table", 
      postgres_conn_id="postgres_local",
      dag=dag
   )

   import_dataset = PostgresOperator(
      sql="sql/import_dataset.sql",
      task_id="import_dataset", 
      postgres_conn_id="postgres_local",
      dag=dag
   )

   insert_dataset_to_table = PostgresOperator(
      sql="sql/insert_dataset_to_table.sql",
      task_id="insert_dataset_to_table", 
      postgres_conn_id="postgres_local",
      dag=dag
   )

   end = DummyOperator(
      task_id="end"
   )

   scrapy_urls = BashOperator(
      task_id="scrapy_urls",
      bash_command="pip install scrapy && scrapy crawl players_urls",
      cwd=dag.folder,
   )

   scrapy_stats = BashOperator(
      task_id="scrapy_stats",
      bash_command="scrapy crawl players_stats",
      cwd=dag.folder,
   )


start >> delete_json >> scrapy_urls >> scrapy_stats >> transform >> drop_table >> create_table >> import_dataset >> insert_dataset_to_table >> end
