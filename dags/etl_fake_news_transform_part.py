from datetime import datetime
from http import client
import pandas as pd
import numpy as np
from minio import Minio
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable

default_args = {"owner" : "airflow",
                "start_date" : datetime(2021,5,1),
                "depends_on_past" : False}

dag = DAG(dag_id= "etl_fake_news_transform_part_project",
        description="Processo de ETL do Projeto focado em Fake News",
        schedule_interval= "@once",
        default_args = default_args)

data_lake_server = Variable.get("data_lake_server")
data_lake_login = Variable.get("data_lake_login")
data_lake_password = Variable.get("data_lake_password")

client = Minio(data_lake_server,
            access_key= data_lake_login,
            secret_key= data_lake_password,
            secure= False)

def _transform():
    df_true = pd.read_parquet("/tmp/etl_true_fakenews.parquet")
    df_fake = pd.read_parquet("/tmp/etl_fake_fakenews.parquet")

    df = pd.merge(df_true, df_fake, how = "outer")

    df['text'] = df['title'] + " " + df['text']

    del df['title']

    df.to_parquet("/tmp/etl_fakenews.parquet")

def _load():

    df = pd.read_parquet("/tmp/etl_fakenews.parquet")

    df.to_parquet("/tmp/etl_fakenews.parquet")

    client.fput_object("processado", 
                        "etl_fakenews.parquet",
                        "/tmp/etl_fakenews.parquet")

transform = PythonOperator(task_id = "transform",
                            python_callable= _transform,
                            provide_context = True,
                            dag = dag)

load = PythonOperator(task_id = "load",
                            python_callable= _load,
                            provide_context = True,
                            dag = dag)

clean = BashOperator(task_id = "clean", 
                    bash_command= "rm -f /tmp/*.parquet",
                    dag = dag)

transform >> load >> clean