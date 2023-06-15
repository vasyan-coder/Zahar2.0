FROM python:3.11
WORKDIR /Zahar2.0/
COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt
COPY ./ ./
CMD ["python", "./bot.py"]