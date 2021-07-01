FROM python:3.8-slim
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && export FLASK_APP=app.py
#COPY . .
# CMD ["flask", "run"]
#EXPOSE 5000