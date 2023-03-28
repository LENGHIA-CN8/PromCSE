# syntax=docker/dockerfile:1
FROM python:3.7-slim-buster

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update
RUN apt-get install -y python-setuptools
RUN apt-get install -y python3-dev
RUN apt-get install -y gcc


RUN adduser --disabled-password myuser
USER myuser
WORKDIR /home/myuser/app
ENV PATH="/home/myuser/.local/bin:${PATH}"


COPY --chown=myuser:myuser requirements.txt requirements.txt


RUN pip install --upgrade pip && pip install --user --no-cache-dir --default-timeout=2000 -r requirements.txt
RUN pip install --user torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


COPY --chown=myuser:myuser . .

WORKDIR /home/myuser/app/src


EXPOSE 19735

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "19735", "--workers", "4", "main_script_2:app"]
