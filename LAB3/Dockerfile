FROM python:3.11
USER root
WORKDIR /app
COPY .. /app/
RUN pip3 install -r requirements.txt
RUN python src/model_fit.py
EXPOSE 8000
LABEL authors="Sergei Lipatov"
ENTRYPOINT ["uvicorn", "app.model_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
