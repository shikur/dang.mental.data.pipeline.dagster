
from dagster import schedule
from dagster_docker import docker_executor
from pipeline_conversation_mentalhealth.job.conversations_mh_pipeline import conversation_etl_op_graph
from dagster import resource

@resource(config_schema={
    "write_file_dir": str,
    "read_file_dir": str,
    "readfilename": str,
    "writefilename": str,
})
def conversations_file_dirs_resource(context):
    return {
        "write_file_dir": context.resource_config["write_file_dir"],
        "read_file_dir": context.resource_config["read_file_dir"],
        "readfilename": context.resource_config["readfilename"],
        "writefilename": context.resource_config["writefilename"],
    }


# # Define the conversation_etl_pipeline job
# conversation_etl_pipeline = conversation_etl_op_graph.to_job(
#     name="conversation_etl_pipeline_mentalhealth",
#     executor_def=docker_executor,
#     resource_defs={"conv_file_dirs": conversations_file_dirs_resource}
# )


conversation_etl_pipeline = conversation_etl_op_graph.to_job(name="conversation_etl_pipeline_mentalhealth", executor_def=docker_executor, resource_defs={"conv_file_dirs": conversations_file_dirs_resource})



# Schedule for conversation_etl_pipeline
@schedule(cron_schedule="0 */2 * * *", job=conversation_etl_pipeline, name="conversation_etl_pipeline_schedule")
def conversation_etl_pipeline_schedule(_context):
    return {}





run_config = {
    "resources": {
        "conv_file_dirs": {
            "config": {
                "read_file_dir": "/opt/dagster/app/pipeline_mentalhealth/data/input/",
                "write_file_dir": "/opt/dagster/app/pipeline_mentalhealth/data/output/",
                "readfilename": "Mental_Health_FAQ.csv",
                "writefilename": "out_Mental_Health_FAQ.csv",
            }
        }

    }
}

