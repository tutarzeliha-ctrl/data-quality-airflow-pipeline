import requests
from airflow.models import Variable

# Airflow UI üzerinden güvenle saklayacağın Slack Webhook URL'ini buraya bağlayabiliriz
# Ya da test için direkt string olarak verebilirsin.
SLACK_WEBHOOK_URL = Variable.get("SLACK_WEBHOOK_URL", default_var="BURAYA_WEBHOOK_URL_GELECEK")

def send_slack_alert(context):
    """
    Airflow task'ı veya kalite kontrolü patladığında Slack'e detaylı hata mesajı gönderir.
    """
    dag_id = context.get('dag').dag_id
    task_id = context.get('task_instance').task_id
    execution_date = context.get('execution_date')
    log_url = context.get('task_instance').log_url

    slack_message = {
        "text": f"🚨 *Data Pipeline Alert*\n\n"
                f"• *DAG:* `{dag_id}`\n"
                f"• *Task:* `{task_id}`\n"
                f"• *Execution Time:* `{execution_date}`\n"
                f"• *Status:* Failed ❌\n"
                f"• <{log_url}|🔗 View Logs>"
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
    
    if response.status_code != 200:
        raise ValueError(f"Slack'e mesaj gönderilemedi, hata kodu: {response.status_code}")