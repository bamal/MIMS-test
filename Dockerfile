FROM python:3
ADD . /crawler_test
WORKDIR /crawler_test
COPY . /crawler_test
COPY . /scrapyd.conf/etc/scrapyd/
EXPOSE 5000
EXPOSE 6800
ENV FLASK_APP=crawler/app.py
ENV PYTHONPATH "${PYTHONPATH}:/crawler_test"
RUN pip install -r requirements.txt
CMD ["scrapyd", "--pidfile="]
#ENTRYPOINT [ "flask"]
#CMD [ "run", "--host", "0.0.0.0"]


