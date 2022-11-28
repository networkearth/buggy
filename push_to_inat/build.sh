#!/bin/bash
if [[ $1 = "dev" ]]
then
docker build --build-arg APP_NAMESPACE=buggy --build-arg APP_ENVIRONMENT=dev --build-arg APP_ACCOUNT=575101084097 --build-arg APP_REGION=us-east-1 --build-arg API_URL=localhost:5002 --platform linux/amd64 -t push-to-inat .
export AWS_PROFILE=deployer
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 575101084097.dkr.ecr.us-east-1.amazonaws.com;
docker tag push-to-inat:latest 575101084097.dkr.ecr.us-east-1.amazonaws.com/push-to-inat:latest;
docker push 575101084097.dkr.ecr.us-east-1.amazonaws.com/push-to-inat:latest;
else
echo "Please specify a valid environment..."
fi