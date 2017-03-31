from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'jonas.cheng',
    'depends_on_past': False,
    'start_date': datetime(2017, 3, 1),
    'email': ['jonas.cheng@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(dag_id='demo', default_args=default_args)
dag.schedule_interval = '@hourly'

# t1, t2, t3 and t4 are examples of tasks created using operators

t1 = BashOperator(
    task_id='collect_account_list',
    bash_command='echo "collect_account_list"',
    dag=dag)

t2 = BashOperator(
    task_id='export_posted_status',
    bash_command='echo "export_posted_status"',
    dag=dag)

t3 = BashOperator(
    task_id='export_liked_status',
    bash_command='echo "export_liked_status"',
    dag=dag)

t4 = BashOperator(
    task_id='export_commentted_status',
    bash_command='echo "export_commentted_status"',
    dag=dag)

t5 = BashOperator(
    task_id='convert_to_tsv',
    bash_command='echo "convert_to_tsv"',
    dag=dag)

t6 = BashOperator(
    task_id='upload_to_s3',
    bash_command='echo "upload_to_s3"',
    dag=dag)

t1 >> t2 >> t5
t1 >> t3 >> t5
t1 >> t4 >> t5
t5 >> t6
