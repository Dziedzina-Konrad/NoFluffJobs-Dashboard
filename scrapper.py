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
         self.job_pages.append([job_key, self.job_url + job["url"]])
      self.mandatory_skills = []
      self.nice_to_have_skills = []

   def get_job_skills(self, link):
      """Get skills from nfj website that is passed as parametr link

      Args:
          link (string): url for website with job details

      Returns:
          array: Return 2 arrays, first with mandatory skills, second with optional skills.
      """
      soup = BeautifulSoup(requests.get(link).text, "html5lib")
      must_have_section = soup.find("section", class_="d-block")
      must_have_skills = []
      try:
         for skill in must_have_section.find_all("li"):
            must_have_skills.append(skill.text.strip())
      except:
         soup = BeautifulSoup(requests.get(link).text, "html5lib")
         must_have_section = soup.find("section", class_="d-block")
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
   
   def job_scrapper_manager(self, jobs_to_download = 0):
      if jobs_to_download == 0:
         pages = self.job_pages
      else:
         pages = self.job_pages[:jobs_to_download]
         
      for job in pages:
         print(f"Scraping data for: {job[1]}")
         mandatory, nice_to_have = self.get_job_skills(job[1])
         mandatory_skills = [job[0], mandatory]
         nice_to_have_skills = [job[0], nice_to_have]
         if mandatory_skills not in self.mandatory_skills:
            self.mandatory_skills.append([job[0], mandatory])
         if nice_to_have_skills not in self.nice_to_have_skills:
            self.nice_to_have_skills.append([job[0], nice_to_have])
            
            
   def create_skills_df(self):
      self.mandatory_df = pd.DataFrame(self.mandatory_skills, columns=["company--title", "skill"])
      self.mandatory_df = self.mandatory_df.explode("skill")
      self.nice_to_have_df = pd.DataFrame(self.nice_to_have_skills, columns=["company--title", "skill"])
      self.nice_to_have_df = self.nice_to_have_df.explode("skill")
      
      
   def skills_to_csv(self, mandatory_csv = "mandatory_skills.csv", nice_to_have_csv = "optional_skills.csv", separator= ";"):
      self.mandatory_df.to_csv(mandatory_csv, sep=separator)
      self.nice_to_have_df.to_csv(nice_to_have_csv,sep=separator)