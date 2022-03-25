FROM python:3.9
ADD . /Flask-Login-Example
WORKDIR /Flask-Login-Example
RUN pip install -r requirements.txt
CMD python app.py
