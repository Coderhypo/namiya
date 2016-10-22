FROM python:2.7

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:4000", "nayami.app_runner:app"]

ENV PYTHONPATH=/app

EXPOSE 4000