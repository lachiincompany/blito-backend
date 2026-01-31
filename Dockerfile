FROM python:3.11-slim

WORKDIR /app

# Use Runflare PyPI mirror inside the build
ARG PIP_INDEX_URL=https://mirror-pypi.runflare.com/simple
ARG PIP_TRUSTED_HOST=mirror-pypi.runflare.com

ENV PIP_INDEX_URL=${PIP_INDEX_URL}
ENV PIP_TRUSTED_HOST=${PIP_TRUSTED_HOST}
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--log-level", "info"]

