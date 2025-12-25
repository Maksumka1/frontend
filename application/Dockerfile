FROM python
WORKDIR /app
COPY crypto.py .

FROM python:alpine
WORKDIR /small
COPY --from=0 /app/crypto.py ./crypto.py
COPY links.json /small/links.json
RUN mkdir logs
RUN pip install --no-cache-dir psycopg2-binary requests beautifulsoup4 lxml prometheus_client
CMD ["python", "crypto.py"]