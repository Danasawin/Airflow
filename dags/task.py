from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime
import random

dag = DAG(
	'even_odd_example',
	start_date=datetime(2023, 1, 1),
	schedule_interval=None, # Set your desired schedule interval
	catchup=False # Set to True if you want to backfill past runs
)

def check_even_odd():
	number = random.randint(1, 100) # Generates a random number between 1 and 100
	if number % 2 == 0:
		return 'branch_even'
	else:
		return 'branch_odd'

branch_even = DummyOperator(task_id='branch_even', dag=dag)
branch_odd = DummyOperator(task_id='branch_odd', dag=dag)

branch_task = BranchPythonOperator(
	task_id='branching',
	python_callable=check_even_odd,
	dag=dag,
)

branch_task >> [branch_even, branch_odd]