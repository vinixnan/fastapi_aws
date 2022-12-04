myregion=$(aws configure get region)
aws ecr create-repository --repository-name fastapi_aws --region $myregion
source update_docker.sh
