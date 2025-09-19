from prefect import flow, task
from tasks.data_extraction import extract_news
from tasks.data_transform import transform_news
from tasks.data_load import load_to_csv, load_to_sqlite

@flow(name="financial_news_etl")
def etl_flow():
    raw_data = extract_news()
    clean_data = transform_news(raw_data)
    load_to_sqlite(clean_data)
    

if __name__ == "__main__":
    etl_flow()
