FROM ubuntu:latest
FROM python:3.10

WORKDIR /app

# Installing pipenv
RUN pip install pipenv
# Copy Pipfile and Pipfile.lock to project directory
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system --deploy && pip freeze

EXPOSE 8501

# Add application's images
RUN mkdir images
ADD app/images/ images/
# Add application's pages
RUN mkdir pages
ADD app/pages/ pages/
ADD app/app_utils.py .

# Add env variables
RUN mkdir .streamlit
ADD app/.streamlit/secrets.toml .streamlit/
ADD app/Home.py .
ADD app/run.sh .

ENTRYPOINT ["bash", "./run.sh"]