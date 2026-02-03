FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]