FROM python:3.8-slim as build
WORKDIR /app

ADD requirements .
RUN pip install -r requirements
ADD . .

FROM build as game-api
EXPOSE 8080
CMD ["python", "app.py"]
