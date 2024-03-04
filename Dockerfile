# Dagster libraries to run both dagster-webserver and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.12-alpine

RUN pip install \
    dagster \
    dagster-graphql \
    dagster-webserver \
    dagster-postgres \ 
    dagster-docker

    #    dagster-aws 

# Set $DAGSTER_HOME and copy dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p $DAGSTER_HOME

# RUN chmod -R 777 ./pipeline_mentalhealth/data/output

# RUN chmod -R 777 /opt/dagster/app/pipeline_mentalhealth/data/output


COPY dagster.yaml workspace.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME
