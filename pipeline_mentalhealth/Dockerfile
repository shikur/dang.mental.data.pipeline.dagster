FROM python:3.12-alpine

# Checkout and install dagster libraries needed to run the gRPC server
# exposing your repository to dagster-webserver and dagster-daemon, and to load the DagsterInstance

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker \
    pandas

# Add repository code

WORKDIR /opt/dagster/app
# RUN mkdir data
COPY . /opt/dagster/app/pipeline_mentalhealth

RUN chmod -R 777 ./pipeline_mentalhealth/data/output

RUN chmod -R 777 /opt/dagster/app/pipeline_mentalhealth/data/output
# COPY dagster_deployment_docker/data /opt/dagster/app/pipeline_mentalhealth

# Run dagster gRPC server on port 4000

EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "pipeline_mentalhealth"]
