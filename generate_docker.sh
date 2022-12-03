#docker build -t fastapi_aws:v1 .
export DOCKER_CLI_EXPERIMENTAL=enabled
docker buildx create --use --name multi-arch-builder
docker buildx build --platform=linux/amd64 -t fastapi_aws:v1 .

myregion=$(aws configure get region)

aws ecr create-repository --repository-name fastapi_aws --region $myregion > creationJson.json
repositoryUri=$(cat creationJson.json | jq ".repository" | jq ".repositoryUri" | xargs)
aws ecr get-login-password --region $myregion | docker login --username AWS --password-stdin $repositoryUri
docker tag fastapi_aws:v1 $repositoryUri:v1
docker push $repositoryUri:v1