FROM python:3.8-slim

RUN pip install boto3

RUN mkdir /src

COPY audit.py /src/

WORKDIR /src

ENTRYPOINT ["python","/src/audit.py"]
CMD ["-h"]
