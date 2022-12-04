export DOCKER_CLI_EXPERIMENTAL=enabled
docker buildx create --use
myregion=$(aws configure get region)
repositoryUri=$(aws ecr describe-repositories --repository-name fastapi_aws | jq -r ".repositories[0].repositoryUri")
echo $repositoryUri at $myregion
aws ecr get-login-password --region $myregion | docker login --username AWS --password-stdin $repositoryUri
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push -t $repositoryUri:v2 \
  -f Dockerfile .