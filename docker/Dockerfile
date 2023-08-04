FROM python:3.10.11-buster
COPY src/ docker/startup.sh /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD bash ./startup.sh
# CMD ["python", "app.py"]
# CMD python app.py
# CMD ["gunicorn", "app:server", "--bind", "127.0.0.1:8080", "--timeout", "120", "--workers", "3"]
