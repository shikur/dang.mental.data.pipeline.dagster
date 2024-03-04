from dagster import op, job, graph
import pandas as pd


@op(required_resource_keys={"file_dirs" })
def read_csv(context) -> pd.DataFrame:
    dirsource = f"{context.resources.file_dirs['read_file_dir']}";
    filenamesource = f"{context.resources.file_dirs['readfilename']}"
    fullpath = dirsource + filenamesource
    context.log.info(fullpath)
    # df = pd.read_csv(fullpath)
    # context.log.info(df.head(10))
    # context.log.info(fullpath)
    # "/opt/dagster/app/pipeline_mentalhealth/data/input/Mental_Health_FAQ.csv"
    return pd.read_csv("/opt/dagster/app/pipeline_mentalhealth/data/input/Mental_Health_FAQ.csv")

@op
def transform_data(context, df: pd.DataFrame) -> pd.DataFrame:
    context.log.info("Transforming data")
    context.log.info(df.head(10))
    return df.head(100)

@op(required_resource_keys={"file_dirs"})
def save_csv(context, df: pd.DataFrame):
    # context.log.info(f"Saving transformed CSV to ")
    # files_in_dir = os.listdir(context.resources.file_dirs["count_file_dir"])
    # context.log.info(f"Total number of files: {len(files_in_dir)}")

    dirsource = f"{context.resources.file_dirs['write_file_dir']}";
    filenamesource = f"{context.resources.file_dirs['writefilename']}"
    fullpath = dirsource + filenamesource

    context.log.info("Transforming data")
    context.log.info(df.head(10))
    context.log.info(fullpath)

    df.to_csv("/opt/dagster/app/pipeline_mentalhealth/data/output/out_Mental_Health_FAQ.csv", index=False)

@graph
def etl_op_graph():
    save_csv(transform_data(read_csv()))
