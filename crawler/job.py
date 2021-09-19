import os
from pathlib import Path
import json
import numpy as np

class Job:

    def __init__(self, job_id):
        """
        Initialize the constructor
        :param job_id: string
            The unique identifier of the job
        """
        self.job_id = job_id
        Path(os.getcwd() + "/data").mkdir(parents=True, exist_ok=True)
        self.result_file = os.getcwd() + '/data/' + job_id+'.pickle'
        self.request_file = os.getcwd() + '/data/' + job_id + '.json'
        self.log_file = os.getcwd() + '/logs/scrapymims/images/' + job_id + '.log'

    def save_job_info(self, data):
        """
        Saves the job creation request in a json file

        :param data: JSON format
            The job creation request
        """
        data.update({'jobid': self.job_id})

        data = json.dumps(data)

        jsonFile = open(self.request_file, "w")

        jsonFile.write(data)

        jsonFile.close()


    def _read_job_attr(self, key):
        '''
        Read the job value associated with key
        :param key: String
            A job request key
        :return:
            The value associated with the attr
        '''

        f = open(self.request_file)

        data = json.load(f)

        content = data[key]

        f.close()

        return content


    def get_job_results(self):
        """
        Get the results of the job
        :return: JSON format
            Returns the job request results
        """
        with open(self.result_file) as f:

            contents = f.read()

            contents = contents.replace('\n', '')

            contents = contents.replace("\'", '"')

            data_json = json.dumps(contents)

            return data_json


    def _get_logs(self):
        """
        Get the job logs

        :return: String
            Returns the job logs
        """

        with open(self.log_file) as f:

            contents = f.read()

            return contents


    def get_status(self, key):
        """
        Fetch the status of a job
        :param key: String
            The key of job request

        :return: dict
            returns the number of URLs that are being crawled ("in progress")
            and the number of URLs for which crawling has completed ("completed")
        """
        logs = self._get_logs() # future work, more details about the crawling job

        list_tasks = self._read_job_attr(key) # get the urls field from the request

        n_tasks = len(list_tasks)

        job_results = self.get_job_results()

        mask = [task in job_results
                for task in list_tasks]

        completed = np.count_nonzero(mask)

        if logs.find('elapsed_time_seconds') != -1: # all jobs finished crawling

            return {
                "completed":n_tasks,
                "in_progress": 0
             }

        in_progress = n_tasks - completed

        return {
            "completed":completed,
            "in_progress":in_progress
        }

