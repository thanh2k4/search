import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from search_engine import insert_document, fetch_articles_batch, delete_document
import requests
from datetime import datetime
import json


def run_spider():
    subprocess.run(
        ["scrapy", "crawl", "new"],
        cwd="C:/Users/Public/Documents/search",
        shell=True
    )

scheduler = BackgroundScheduler()
scheduler.add_job(
    run_spider,
    trigger="interval",
    hours=12,
    id="scrapy_new_spider",
    replace_existing=True
)


STATE_FILE = "last_crawl_time.json"

def load_last_time():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("last_time")
    except FileNotFoundError:
        return None

def save_last_time(last_time):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_time": last_time}, f, ensure_ascii=False)

def parse_time(time_str):
    dt = datetime.strptime(time_str.split(" (")[0], "%A, %d/%m/%Y, %H:%M")
    return dt

def crawl_article(link):
    try:
        r = requests.head(link, timeout=10)
        return r.status_code != 404
    except requests.RequestException:
        return False

def crawl_and_update_articles():
    last_time = load_last_time()
    while True:
        articles = fetch_articles_batch(last_time=last_time, batch_size=50)
        if not articles:
            break

        for hit in articles:
            doc = hit["_source"]
            link = doc["link"]
            last_time = doc["time"]
            if not crawl_article(link):
                delete_document(link)

    if last_time:
        save_last_time(last_time)


scheduler.add_job(
    crawl_and_update_articles,
    trigger="interval",
    hours=3,
    id="es_crawl_update",
    replace_existing=True
)

scheduler.start()
