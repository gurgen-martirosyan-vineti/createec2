FROM python:3
WORKDIR /app
COPY createec2.py ./
RUN pip install awscli boto3

CMD [ "python", "./create_ec2.py" ]