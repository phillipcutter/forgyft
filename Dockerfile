FROM python:3

#WORKDIR /usr/src/app
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
#COPY . .

RUN mkdir app
COPY app/requirements.txt /app

RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 80

WORKDIR /app

COPY . /app

# CMD ["./start.sh"]