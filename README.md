
Crawler test
======================

Crawler test is a web application developed in python.It extracts **image URLs** from the web. This library is built on a high-level web crawling and web scraping framework called **scrapy**.
All further details ca be found [here](https://docs.google.com/document/d/12YYKsnUsXvOQocI3stx6cn-YYGWdYdi8M0UY1rjmQiw/edit?usp=sharing). 

How to run the Crawler
--------------------------

To run the test on your localhost:

```
$ git clone https://github.com/bamal/MIMS-test.git
$ cd MIMS-test-master
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ {your current working directory}/venv/bin/python -m flask run

```
Open another Terminal and start the **scrapyd** server (by default it runs on port 6800).

```
$ cd cd MIMS-test-master
$ source venv/bin/activate
$ scrapyd
```

This application has three endpoints: 

* To start crawling your urls and parsing their images urls, this is an example of a POST request: 

```
curl -X POST 'http://localhost:5000/jobs' -H "Content-Type: application/json" -d '{"urls":["http://4chan.org/", "https://golang.org/"], "workers":2'}
```

* To get the status of your job, this is an example of a GET request:

```
curl -X GET 'http://localhost:5000/jobs/c25b020a19b011ecb282a504b09ff6d8/status'
```

* To get the result of your job, this is an example of a GET request:

```
curl -X GET 'http://localhost:5000/jobs/c25b020a19b011ecb282a504b09ff6d8/result'

```
 Here ``jobid`` = c25b020a19b011ecb282a504b09ff6d8

