import pandas as pd
import requests,json
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
      self.mandatory_df = pd.DataFrame(columns=["Company--title", "Skill"])
      self.nice_to_have_df =  pd.DataFrame(columns=["Company--title", "Skill"])
      self.job_pages = [] # List of company-title and url
      self.unique_keys = [] # List of unique company--title 
      self.unique_jobs = [] # List of list unique company--title keyand links 
      self.non_working_urls = []
      
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
         
         has_data = job[0] in self.mandatory_df["Company--title"].values
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
      for url in self.non_working_urls: print(f"Non working url: {url}")
            
            
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
         self.non_working_urls.append(link)
         print(f"Non working link: {link}")
      nice_to_have_skills = []
      try:
         nice_to_have_section = soup.find("section" , class_="d-block mt-3 ng-star-inserted")
         for skill in nice_to_have_section.find_all("li"):
            nice_to_have_skills.append(skill.text.strip())
      except:
         print(f"No nice to have data for: {link}")
      return must_have_skills, nice_to_have_skills
   
   
   def create_skills_df(self):
      """Create dataframes from mandatory_skills and nice_to_have_skills.\n
      Dataframes are saved as self.mandatory_df and self.nice_to_have_df.
      """
      for data in self.mandatory_skills:
         temp_df = pd.DataFrame({
            'Company--title': [data[0]] * len(data[1]),
            'Skill': data[1]
         })
         self.mandatory_df = pd.concat([self.mandatory_df, temp_df])
         
         
      for data in self.nice_to_have_skills:
         temp_df = pd.DataFrame({
            'Company--title': [data[0]] * len(data[1]),
            'Skill': data[1]
         })
         self.nice_to_have_df = pd.concat([self.nice_to_have_df, temp_df])
         
      
   def skills_to_csv(self, mandatory_csv = "mandatory_skills.csv", nice_to_have_csv = "optional_skills.csv", separator= ";"):
      """Saving data of skills to files.

      Args:
          mandatory_csv (str, optional): file name for mandatory dataframe. Defaults to "mandatory_skills.csv".
          nice_to_have_csv (str, optional): file name gor optional/nice to have datarframe. Defaults to "optional_skills.csv".
          separator (str, optional): Seperator that is used for creating files. Defaults to ";".
      """
      self.mandatory_df.to_csv(mandatory_csv, sep=separator, index=False)
      self.nice_to_have_df.to_csv(nice_to_have_csv,sep=separator, index=False)
   
   
   def load_saved_files(self, mandatory_csv="test\\mandatory_safe_point.csv", nice_to_have_csv="test\\optional_safe_point.csv", sep=";"):
      """Load files and update mandatory_df and nice_to_have_df

      Args:
          mandatory_csv (str, optional): File to load mandatory data. Defaults to "test\mandatory_safe_point.csv".
          nice_to_have_csv (str, optional): File to load nice to have data. Defaults to "test\optional_safe_point.csv".
          sep (str, optional): Seperator of file. Defaults to ";".
      """
      mandatory = pd.read_csv(mandatory_csv, sep=sep , index_col = False)
      self.mandatory_df = pd.concat([self.mandatory_df, mandatory])
      print("Loading nice to have data.")
      nice_to_have = pd.read_csv(nice_to_have_csv, sep=sep , index_col = False)
      self.nice_to_have_df = pd.concat([nice_to_have, self.nice_to_have_df])
      print("Loading saved files completed.")
      
   def clean_df(self):
      """ Use for cleaning data from non-actual jobs.
      """
      mandatory = self.mandatory_df
      nice_to_have = self.nice_to_have_df
      self.mandatory_df = mandatory[mandatory["Company--title"].isin(self.unique_keys)]
      self.nice_to_have_df = nice_to_have[nice_to_have["Company--title"].isin(self.unique_keys)]
      