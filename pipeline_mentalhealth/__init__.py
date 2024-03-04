
from dagster import schedule, Definitions, EnvVar
from dagster_docker import docker_executor
from pipeline_mentalhealth.job.freq_mh_pipeline import etl_op_graph
from dagster import resource


@resource(config_schema={
    "write_file_dir": str,
    "read_file_dir": str,
    "readfilename": str,
    "writefilename": str,
})
def file_dirs_resource(context):
    return {
        "write_file_dir": context.resource_config["write_file_dir"],
        "read_file_dir": context.resource_config["read_file_dir"],
        "readfilename": context.resource_config["readfilename"],
        "writefilename": context.resource_config["writefilename"],
    }



etl_pipeline = etl_op_graph.to_job(
    name="etl_pipeline_mentalhealth",
    executor_def=docker_executor,
    resource_defs={"file_dirs": file_dirs_resource}
)


etl_pipeline = etl_op_graph.to_job(name="etl_pipeline_mentalhealth", executor_def=docker_executor, resource_defs={"file_dirs": file_dirs_resource})


# Schedule for etl_pipeline
@schedule(cron_schedule="* * * * *", job=etl_pipeline, name="etl_pipeline_schedule")
def etl_pipeline_schedule(_context):
    return {}





run_config = {
    "resources": {
        "file_dirs": {
            "config": {
                "read_file_dir": "/opt/dagster/app/pipeline_mentalhealth/data/input/",
                "write_file_dir": "/opt/dagster/app/pipeline_mentalhealth/data/output/",
                "readfilename": "Mental_Health_FAQ.csv",
                "writefilename": "out_Mental_Health_FAQ.csv",
            }
        }

    }
}

