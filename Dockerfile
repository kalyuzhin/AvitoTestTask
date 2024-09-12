FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080

CMD [ "flask", "-A", "avito", "run", "--host=0.0.0.0", "--port=8080"]