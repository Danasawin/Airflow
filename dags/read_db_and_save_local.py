from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
import csv
import pandas as pd
from datetime import datetime
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,  # Changed 'depend_on_past' to 'depends_on_past'
    'email': ['airflow@example.com']
}

def reading_data():
    request = "SELECT * FROM Customer"
    mysql_hook = MySqlHook(mysql_conn_id = 'mydb', schema = 'homestead')
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    sources = cursor.fetchall()
    df = pd.DataFrame(sources,columns=[desc[0] for desc in cursor.description])
    return df

def save_to_csv():
    df = reading_data()
    dir = '/my_tmp/airflow.csv'
    df.to_csv(dir,index=True)

 

with DAG(
    'read_db_and_save_local',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['airflow_tab'],
) as dag:
    start = DummyOperator(
        task_id='start'
    )

    end = DummyOperator(
        task_id='end'
    )

    read_db = PythonOperator(
        task_id='read_db',
        python_callable=reading_data
    )
    save_csv = PythonOperator(
        task_id = 'save_csv',
        python_callable=save_to_csv
    )

    start >> read_db >> save_csv >> end