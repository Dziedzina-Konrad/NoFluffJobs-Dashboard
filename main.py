from scrapper import NoFluffJobs

nfj = NoFluffJobs()
print(f"{len(nfj.unique_jobs)}: {len(nfj.job_pages)}")
nfj.job_scrapper_manager()
print(nfj.mandatory_skills)
print(nfj.nice_to_have_skills)
nfj.create_skills_df()
nfj.skills_to_csv()