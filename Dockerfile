FROM tiangolo/uvicorn-gunicorn:python3.7

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./models /models
COPY ./app /app

# docker build -f Dockerfile --no-cache -t nk3466/nl_inference:0.0.2 .
# docker build -f Dockerfile -t nl_inference:0.0.1 .
# docker images
# docker run -it --rm -p 8000:80 -e MAX_WORKERS=2 nk3466/nl_inference:0.0.1
# docker image prune
# docker push
# docker exec -it --user root 0e08 /bin/bash