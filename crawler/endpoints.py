import socket
import numpy as np
from flask import request
from joblib import Parallel, delayed
from scrapyd_api import ScrapydAPI
from crawler.job import Job


def configure_endpoints(app):

    @app.route('/')
    def hello():
        return 'I am on Host: ' + socket.gethostbyname(socket.gethostname())


    @app.route('/jobs', methods=['POST'])
    def crawl_request():
        """
        The first endpoint of the crawler:

        Schedule different jobs and run them on different threads
        Each job extracts the URL images from the input URLs.

        :return: JSON format files including each:
            "Job id": A unique identifier for the job
            "Urls": The list of urls allocated for each job,
            the input jobs are subdivided on workers
        """
        try:

            data = request.json

            urls = data["urls"]

            urls = np.asarray(urls)

            print(urls)

            # Subdivide the urls to be processed by different workers
            slices = [slice(start, start + data["workers"])
                      for start in range(0, urls.shape[0], data["workers"])]

            # Connect to the scrapyd API (the server should be already running using the scrapyd command)
            scrapyd = ScrapydAPI('http://localhost:6800')

            if data["workers"] == 1 or data["workers"] > len(urls):

                #data["workers"] = 1

                # Schedule spider a run (also known as a job), returning the job id.
                job_id = scrapyd.schedule('scrapymims', 'images', urls=','.join(urls))

                job = Job(job_id)

                data = {"urls": urls}

                job.save_job_info(data)

            else:

                # Schedule Spiders (or jobs) on different threads each having few urls to crawl,
                # each spider/ job has its job id
                requests = Parallel(n_jobs=data["workers"], prefer="threads")(delayed(scrapyd.schedule)
                                                            ('scrapymims', 'images', urls=','.join(urls[slices[i]]))
                                                                              for i in range(len(slices)))

                # Save a JSON file format to keep the request details (Id of each job, urls associated with each job id)
                # This is useful in case we want to extend this application
                for i in range(len(slices)):

                    job_id= requests[i]

                    job = Job(job_id)

                    urls_job = urls[slices[i]]

                    print(urls_job)

                    data = {"urls": urls_job.tolist()}

                    job.save_job_info(data)

            return data

        except:

            raise


    @app.route('/jobs/<job_id>/status', methods=['GET'])
    def fetch_status(job_id):
        """
        Second endpoint for the crawler
        Returns the job status
        :param job_id: String
            The job identifier
        :return: Dict
            returns the number of URLs that are being crawled ("in progress")
            and the number of URLs for which crawling has completed ("completed")
        """
        job = Job(job_id)

        return job.get_status("urls")

    @app.route('/jobs/<job_id>/result', methods=['GET'])
    def fetch_results(job_id):
        """
        Returns the crawling results

        :param job_id: String
            The job identifier

        :return: JSON format
            Returns the job request results
            with (key, value) = (url: [urls images])
        """
        try:

            job = Job(job_id)

            return job.get_job_results()

        except:

            return "404: There is something wrong"


