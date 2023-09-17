from scrapper import NoFluffJobs

nfj = NoFluffJobs()
print(f"{len(nfj.unique_jobs)}: {len(nfj.job_pages)}")
nfj.load_saved_files()
print(nfj.mandatory_skills)
nfj.job_scrapper_manager(skip_loaded_data=True)
print(nfj.mandatory_skills)
print(nfj.nice_to_have_skills)
nfj.create_skills_df()
nfj.skills_to_csv()