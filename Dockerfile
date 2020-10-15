FROM python:3
RUN apt-get update && apt-get install -y ffmpeg
ADD requirements.txt /
RUN pip install -r /requirements.txt
RUN mkdir /app
COPY . /app
WORKDIR /app
CMD ["python", "/app/wololo.py"]
