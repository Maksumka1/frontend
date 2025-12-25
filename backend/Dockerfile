FROM python
WORKDIR /app1
COPY app.py .

FROM python:slim
WORKDIR /small
COPY --from=0 /app1/app.py ./app.py
COPY templates/ templates/
RUN mkdir logs
RUN pip install --no-cache-dir psycopg2-binary flask prometheus_client
EXPOSE 5000
CMD ["python", "app.py"]