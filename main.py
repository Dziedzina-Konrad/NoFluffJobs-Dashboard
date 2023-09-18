from scrapper import NoFluffJobs

nfj = NoFluffJobs()
print(f"{len(nfj.unique_jobs)}: {len(nfj.job_pages)}")
nfj.load_saved_files()
nfj.job_scrapper_manager(skip_loaded_data=True)
nfj.create_skills_df()
nfj.skills_to_csv()
print(nfj.non_working_urls)