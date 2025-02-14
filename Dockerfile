FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install pip-tools && pip-sync requirements.txt

RUN playwright install --with-deps

COPY . .

ENV SHB_DOCKER=TRUE

CMD ["python", "-m", "py_shb_export"]
