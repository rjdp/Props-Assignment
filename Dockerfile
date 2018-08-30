FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system 
COPY . .

#ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "fylehqtest.wsgi"]
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000