from dagster import op, job, graph
import pandas as pd


@op(required_resource_keys={"conv_file_dirs" })
def conversation_read_csv(context) -> pd.DataFrame:
    dirsource = f"{context.resources.file_dirs['read_file_dir']}";
    filenamesource = f"{context.resources.file_dirs['readfilename']}"
    fullpath = dirsource + filenamesource
    context.log.info(fullpath)
    df = pd.read_csv(fullpath)
    context.log.info(df.head(10))
    context.log.info(fullpath)
    # "/opt/dagster/app/pipeline_mentalhealth/data/input/Mental_Health_FAQ.csv"
    return df

@op
def conversation_transform_data(context, df: pd.DataFrame) -> pd.DataFrame:
    context.log.info("Transforming data")
    context.log.info(df.head(10))
    return df.head(100)

@op(required_resource_keys={"conv_file_dirs"})
def conversation_save_csv(context, df: pd.DataFrame):
    dirsource = f"{context.resources.file_dirs['write_file_dir']}";
    filenamesource = f"{context.resources.file_dirs['writefilename']}"
    fullpath = dirsource + filenamesource

    context.log.info("Transforming data")
    context.log.info(df.head(10))
    context.log.info(fullpath)

    df.to_csv(fullpath, index=False)

@graph
def conversation_etl_op_graph():
    conversation_save_csv(conversation_transform_data(conversation_read_csv()))
