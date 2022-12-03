docker buildx build --platform=linux/amd64 -t fastapi_aws:v1 .
myregion=$(aws configure get region)
repositoryUri=$(aws ecr describe-repositories --repository-name fastapi_aws | jq -r ".repositories[0].repositoryUri")
echo $repositoryUri at $myregion
aws ecr get-login-password --region $myregion | docker login --username AWS --password-stdin $repositoryUri
docker tag fastapi_aws:v1 $repositoryUri:v1
docker push $repositoryUri:v1