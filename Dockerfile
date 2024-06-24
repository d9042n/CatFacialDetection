FROM python:3.12

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libgl1-mesa-dev \
  && apt-get install -y libglib2.0-0 \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]