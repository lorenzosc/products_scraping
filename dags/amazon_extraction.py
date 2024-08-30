from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import sqlite3
from scraper.amazon_scraping import AmazonScrape

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def scrape_amazon_prices():
    amazon = AmazonScrape()
    amazon.get_and_save_objects('Cadeira Gamer')
    amazon.close()

dag = DAG(
    'scrape_amazon_prices',
    default_args=default_args,
    description='Scrape gaming chairs prices from Amazon daily',
    schedule_interval=timedelta(days=1),
)

t1 = PythonOperator(
    task_id='scrape_amazon_prices',
    python_callable=scrape_amazon_prices,
    dag=dag,
)