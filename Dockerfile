FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --force-reinstall setuptools>=70.0.0 && \
    python -c "import pkg_resources; print('pkg_resources OK')"

COPY . .

EXPOSE ${PORT:-5500}

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-5500}
