import pandas as pd
import requests
import json
class NoFluffJobs():
   """Class for scrapping and transform data for BI purpose."""
   def __init__(self):
      """url - all jobs on the portal\n
      job_url - first part of link to job details \n"""
      self.url = "https://nofluffjobs.com/api/posting"
      self.job_url = "https://nofluffjobs.com/job/"
      req = requests.get(self.url)
      nfj_jobs = json.loads(req.text)
      nfj_jobs = nfj_jobs["postings"]