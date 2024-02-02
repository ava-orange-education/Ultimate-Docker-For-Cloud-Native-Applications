#!/bin/bash -ex

# Will be mounted to the app as files
docker config create app-config ./app-config.txt | true
docker secret create app-secret ./app-secret.txt | true

# Run the service but don't wait for it
docker service create \
  --name mastering-docker \
  --detach \
  --config source=app-config,uid=1000,gid=1000,mode=0440,target=/app-config.txt \
  --secret source=app-secret,uid=1000,gid=1000,mode=0440,target=/app-secret.txt \
  --user 1000:1000 \
  --restart-condition none \
  busybox sh -c "hostname && cat /app-config.txt /app-secret.txt" | true

# See the details of the running service
docker service inspect mastering-docker

# See the logs of the service, prepending the container hostname and node name
docker service logs mastering-docker

# What are the running services?
docker service ls

# What are the tasks of the service?
docker service ps mastering-docker

# Update the service, updating the image
docker service update --detach --image busybox:1.36 mastering-docker

# See the logs again
docker service logs mastering-docker

# Rollback the latest change (reverting to the old image)
docker service rollback -d mastering-docker

# Scale the app to three
docker service scale -d mastering-docker=3

# See the logs again
docker service logs mastering-docker

# Finally, remove the service
docker service rm mastering-docker
