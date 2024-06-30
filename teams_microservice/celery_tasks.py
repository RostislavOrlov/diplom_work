from main import app
import requests


@app.celery.task
def send_log_file():
    url = "http://localhost:8090/send_log_file"
    with open('app.log') as log_file:
        response = requests.post(url, data=log_file)


@app.celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60*60*24, send_log_file.s(), name="send_log_file")
