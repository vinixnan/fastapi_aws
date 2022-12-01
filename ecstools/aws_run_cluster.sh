repositoryUri=$(cat creationJson.json | jq ".repository" | jq ".repositoryUri" | xargs)
repositoryUri=$repositoryUri:v1 python updateconfig.py
aws ecs create-cluster --cluster-name fargate-cluster > clusterCreation.json
aws ecs register-task-definition --cli-input-json file://ecs_task.json