FROM python:latest
WORKDIR home/misha/Desktop/gdesear_CS446_PA4
COPY pythonCode1.py ./
COPY requirements.txt ./
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
CMD ["python", "./pythonCode1.py"]
