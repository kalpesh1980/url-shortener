FROM ubuntu:18.04

LABEL name='dellus'
LABEL version='1.0.0'
LABEL description='Dellus(pygy.co) URL shortener'
LABEL vendor="Kalpesh Tandel"

RUN apt update && apt install python3-pip -y
RUN mkdir /var/log/dellus

WORKDIR /dellus
ADD ./requirements.txt /dellus/requirements.txt
RUN pip3 install -r requirements.txt --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
ADD . /dellus

EXPOSE 8000

CMD ["python3", "run.py"]
