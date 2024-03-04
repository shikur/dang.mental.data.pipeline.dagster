#!/bin/bash

# Define an associative array where keys are the image names and values are the paths to their Dockerfiles
declare -A dockerfiles=(["pipeline_mentalhealth"]="./pipeline_mentalhealth/Dockerfile" ["pipeline_conversation_mentalhealth"]="./pipeline_conversation_mentalhealth/Dockerfile"  ["dagster"]="./Dockerfile")

log_file="build.log"
touch $log_file

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $log_file
}


# Iterate over the associative array to build each Docker image
for image in "${!dockerfiles[@]}"; do
    dockerfile_path=${dockerfiles[$image]}   
    log_message "Changing to directory $dockerfile_path "
    cd "$dockerfile_path" || { log_message "Failed to change directory to $dockerfile_path . Skipping."; continue; }
    cd ..
    # Extract the directory name to use as the image tag
    image_tag=$(basename "$dockerfile_path")
    
    log "Building Docker image $image from Dockerfile at $dockerfile_path"
    
    if docker build -t $image -f $dockerfile_path .; then
        log "Successfully built $image"
    else
        log "Error building $image. Check $log_file for details."
        exit 1
    fi
done

log "Attempting to run docker-compose up"

# Run docker-compose up and build if necessary
if docker-compose up -d --build; then
    log "docker-compose up executed successfully"
else
    log "Error executing docker-compose up. Check $log_file for details."
    exit 1
fi
