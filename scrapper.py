import pandas as pd
import requests,json, asyncio, aiohttp
from bs4 import BeautifulSoup

class NoFluffJobs():
   """Class for scrapping and transform data for BI purpose."""
   def __init__(self):
      """url - all jobs on the portal\n
      job_url - first part of link to job details \n
      job_pages - list of dictionaries with company--title key. 
      """
      self.url = "https://nofluffjobs.com/api/posting"
      self.job_url = "https://nofluffjobs.com/job/"
      req = requests.get(self.url)
      nfj_jobs = json.loads(req.text)
      nfj_jobs = nfj_jobs["postings"]
      self.job_pages = []
      for job in nfj_jobs:
         job_key = job["name"].strip() + "--" + job["title"].strip()
         job_url = self.job_url + job["url"]
         self.job_pages.append([job_key, self.job_url + job["url"]])

   def get_job_skills(self, link):
      soup = BeautifulSoup(requests.get(link).text)
      must_have_section = soup.find("section", class_="d-block")
      must_have_skills = []
      for skill in must_have_section.find_all("li"):
         must_have_skills.append(skill.text.strip())
      
      nice_to_have_skills = []
      try:
         nice_to_have_section = soup.find("section" , class_="d-block mt-3 ng-star-inserted")
         for skill in nice_to_have_section.find_all("li"):
            nice_to_have_skills.append(skill.text.strip())
      except:
         print(f"No nice to have data for: {link}")
         
      return must_have_skills, nice_to_have_skills