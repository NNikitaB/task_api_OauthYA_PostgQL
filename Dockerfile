FROM python:3.12.4
WORKDIR /code
RUN mkdir -p ./test/
RUN mkdir -p ./internal/
COPY internal/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./internal ./internal/
COPY ./test /test/
EXPOSE 8080
CMD ["uvicorn", "internal.main.app:app","--host", "0.0.0.0", "--port", "8080"]

