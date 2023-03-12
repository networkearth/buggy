#!/bin/bash
if [[ $1 = "local" ]]
then
docker build --build-arg INATURALIST_API=http://44.212.148.112:4000/v1 --build-arg INATURALIST_WEBAPP=http://44.212.148.112:3000 --build-arg BUGGY_BACKUP_PATH=buggy-backups --platform linux/amd64 -t buggy-local-api .
docker run -it -p 5002:5002 buggy-local-api
else
echo "Please specify a valid environment..."
fi