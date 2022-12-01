import json
import os

image_url = str(os.environ['repositoryUri'])

with open('sample_ecs_task.json', 'r') as f:
    data = json.load(f)

data["containerDefinitions"][0]["image"] = image_url

with open("ecs_task.json", "w") as outfile:
    json.dump(data, outfile)
