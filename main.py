from scrapper import NoFluffJobs

nfj = NoFluffJobs()
print(f"{len(nfj.unique_jobs)}: {len(nfj.job_pages)}")
nfj.load_saved_files("mandatory_skills.csv", "optional_skills.csv")
#nfj.job_scrapper_manager(skip_loaded_data=True)
#nfj.create_skills_df()
nfj.clean_df()
nfj.skills_to_csv("mandatory_skills.csv", "optional_skills.csv")
print(nfj.non_working_urls)