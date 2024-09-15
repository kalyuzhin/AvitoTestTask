FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV POSTGRES_CONN=postgresql://cnrprod1725782375-team-77723:cnrprod1725782375-team-77723@rc1b-5xmqy6bq501kls4m.mdb.yandexcloud.net:6432/cnrprod1725782375-team-77723
ENV POSTGRES_USERNAME=cnrprod1725782375-team-77723
ENV POSTGRES_PASSWORD=cnrprod1725782375-team-77723
ENV POSTGRES_DATABASE=cnrprod1725782375-team-77723
ENV POSTGRES_PORT=6432
ENV POSTGRES_HOST=rc1b-5xmqy6bq501kls4m.mdb.yandexcloud.net
EXPOSE 8080

#CMD [ "flask", "-A", "avito", "run", "--port=8080"]
CMD ["python", "run.py"]