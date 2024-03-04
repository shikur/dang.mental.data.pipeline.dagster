# from dagster import job
# # Assuming `job_a` and `job_b` are your Dagster jobs imported from their respective modules
# from pipeline_a import job_a
# from pipeline_b import job_b

# @job
# def etl_pipeline():
#     job_a_result = job_a.execute_in_process()
#     job_b_result = job_b.execute_in_process()
#     return job_a_result, job_b_result  # Adjust based on how you want to handle results