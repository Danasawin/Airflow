from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import pandas as pd

def change_datatype():
    df = pd.read_csv('/my_tmp/tested.csv')
    convert_dict = {'Pclass': float}
    df = df.astype(convert_dict)
    df.to_csv('/my_tmp/tested_2.csv')
def filter_male():
    df = pd.read_csv('/my_tmp/tested.csv')
    df = df[df['Sex'] == 'male']

def save_data():
    df = pd.read_csv('/my_tmp/tested_2.csv')  # Changed '.read.csv' to '.read_csv'

    df.to_parquet('/my_tmp/titanic_lab.parquet', engine='fastparquet')



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,  # Changed 'depend_on_past' to 'depends_on_past'
    'email': ['airflow@example.com']
}

with DAG(
    'dataframe_lab1',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['airflow_tab'],
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')
    
    change_datatype_task = PythonOperator(
        task_id='change-datatype',
        python_callable=change_datatype
    )
    filter_male = PythonOperator(
        task_id ='filter_male',
        python_callable=filter_male
    )
    
    save_data_task = PythonOperator(
        task_id='save_data',  # Corrected 'tassk_id' to 'task_id'
        python_callable=save_data
    )
    
    start >> change_datatype_task >> filter_male >> save_data_task >> end
