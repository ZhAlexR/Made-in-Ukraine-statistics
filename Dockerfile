FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron procps

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
COPY data_parser/ app/data_parser

RUN chmod +x /app/setup_cron.sh

CMD python3 /app/data_parser/main.py && /app/setup_cron.sh && streamlit run /app/dashboard.py & tail -f /dev/null
