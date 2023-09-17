import time
import pandas as pd
import requests,json, threading
from bs4 import BeautifulSoup

class NoFluffJobs():
   """Class for scrapping skills information of every jobs or unique jobs*"""
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
      self.job_pages = [] # List of company-title and url
      self.unique_keys = []
      self.unique_jobs = []
      self.loaded_keys = []
      
      for job in nfj_jobs:
         job_key = job["name"].strip() + "--" + job["title"].strip()
         self.job_pages.append([job_key, self.job_url + job["url"]])
         if job_key not in self.unique_keys:
            self.unique_jobs.append([job_key, self.job_url + job["url"]])
            self.unique_keys.append(job_key)
      self.mandatory_skills = []
      self.nice_to_have_skills = []
   
   
   def job_scrapper_manager(self, jobs_to_download = 0, unique = True, save_point = 100, skip_loaded_data = False):
      """Func for managment of scraping process.

      Args:
          jobs_to_download (int, optional): Parametr for how many jobs skills you want download. Defaults to 0.
          unique (bool, optional): Change if you want download all jobs offerts, not only for unique keys.. Defaults to True.
          save_point (int, optional): Determinate which itteration do save point in test folder. Defaults to 200.
      """
      # Check which data will be loaded
      if unique:
         pages = self.unique_jobs
      else:
         pages = self.job_pages
         
      if jobs_to_download != 0:
         pages = pages[:jobs_to_download]
         
      cnt = 1
      cnt_all = len(pages)
      for job in pages:
         # Check if data are loaded.
         
         has_data = job[0] in self.loaded_keys
         if has_data & skip_loaded_data:
            print(f"Skipped {job[0]} data")
            cnt += 1
            continue
         
         print(f"Scraping data for: {job[1]} \t {cnt}/{cnt_all}")
         mandatory, nice_to_have = self.get_job_skills(job[1])
         mandatory_skills = [job[0], mandatory]
         nice_to_have_skills = [job[0], nice_to_have]
         
         # Preventing duplicates
         if mandatory_skills not in self.mandatory_skills:
            self.mandatory_skills.append([job[0], mandatory])
         if nice_to_have_skills not in self.nice_to_have_skills:
            self.nice_to_have_skills.append([job[0], nice_to_have])
            
         # 
         if(cnt % save_point == 0):
            self.create_skills_df()
            self.skills_to_csv("test\\mandatory_safe_point.csv", "test\\optional_safe_point.csv")
            print("Saved data")
         cnt += 1
            
            
   def get_job_skills(self, link):
      """Get skills from nfj website that is passed as parametr link

      Args:
          link (string): url for website with job details

      Returns:
          array: Return 2 arrays, first with mandatory skills, second with optional skills.
      """
      request = requests.get(link)
      soup = BeautifulSoup(request.text, "html5lib")
      must_have_section = soup.find("section", {"class": "d-block"})
      must_have_skills = []
      try:
         skill_elements =  must_have_section.find_all("li")
         for skill in skill_elements:
            must_have_skills.append(skill.text.strip())
      except:
         print(soup.find_all("li"))
         time.sleep(10)
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
   
   
   def create_skills_df(self):
      self.mandatory_df = pd.DataFrame(self.mandatory_skills, columns=["company--title", "skill"])
      self.mandatory_df = self.mandatory_df.explode("skill")
      self.nice_to_have_df = pd.DataFrame(self.nice_to_have_skills, columns=["company--title", "skill"])
      self.nice_to_have_df = self.nice_to_have_df.explode("skill")
      
      
   def skills_to_csv(self, mandatory_csv = "mandatory_skills.csv", nice_to_have_csv = "optional_skills.csv", separator= ";"):
      """Saving data of skills to files.

      Args:
          mandatory_csv (str, optional): file name for mandatory dataframe. Defaults to "mandatory_skills.csv".
          nice_to_have_csv (str, optional): file name gor optional/nice to have datarframe. Defaults to "optional_skills.csv".
          separator (str, optional): Seperator that is used for creating files. Defaults to ";".
      """
      self.mandatory_df.to_csv(mandatory_csv, sep=separator)
      self.nice_to_have_df.to_csv(nice_to_have_csv,sep=separator)
   
   
   def load_saved_files(self, mandatory_csv="test\\mandatory_safe_point.csv", nice_to_have_csv="test\\optional_safe_point.csv", sep=";"):
      print("Loading mandatory data.")
      mandatory = pd.read_csv(mandatory_csv, sep=sep , index_col = False)
      mandatory = mandatory.groupby("company--title").agg({"skill":list})
      mandatory_array = []
      for row in mandatory.iterrows():
         row_one = row[1].values.tolist()
         print(row_one)
         mandatory_array.append([row[0], row_one])
         self.loaded_keys.append(row[0])
      self.mandatory_skills = mandatory_array
      
      print("Loading nice to have data.")
      optional = pd.read_csv(nice_to_have_csv, sep=sep , index_col = False)
      optional = optional.groupby("company--title").agg({"skill":list})
      optional_array = []
      for row in optional.iterrows():
         optional_array.append([row[0], row[1]])
      self.nice_to_have_skills = optional_array
      print("Loading saved files completed.")