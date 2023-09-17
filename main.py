from scrapper import NoFluffJobs

nfj = NoFluffJobs()
nfj.job_scrapper_manager(100)
print(nfj.mandatory_skills)
print(nfj.nice_to_have_skills)
nfj.create_skills_df()
nfj.skills_to_csv()