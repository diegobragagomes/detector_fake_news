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

dag = DAG(dag_id= "etl_fake_news_fake_part_project",
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

def _extract_fake():

    df_fake = pd.DataFrame(data = None)

    objects = client.list_objects("bruto", prefix = "Fake",recursive = True)

    for object in objects:

        object =  client.get_object(object.bucket_name,
                object.object_name.encode('utf-8'))

        df_fake = pd.read_csv(object)

    df_fake.to_parquet("/tmp/etl_fake_fakenews.parquet")


def _transform_fake():

    df_fake = pd.read_parquet("/tmp/etl_fake_fakenews.parquet")

    df_fake["Status"] = "False"

    df_fake.to_parquet("/tmp/etl_fake_fakenews.parquet")


extract_fake = PythonOperator(task_id = "extract_fake",
                            python_callable= _extract_fake,
                            provide_context = True,
                            dag = dag)

transform_fake = PythonOperator(task_id = "transform_fake",
                            python_callable= _transform_fake,
                            provide_context = True,
                            dag = dag)

extract_fake>> transform_fake