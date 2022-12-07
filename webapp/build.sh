#!/bin/bash
if [[ $1 = "dev" ]]
then
docker build --build-arg APP_NAMESPACE=buggy --build-arg APP_ENVIRONMENT=dev --build-arg APP_ACCOUNT=575101084097 --build-arg APP_REGION=us-east-1 --build-arg API_URL=https://buggy.dev.api.networkearth.io --platform linux/amd64 -t buggy-dev-webapp .
export AWS_PROFILE=deployer
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 575101084097.dkr.ecr.us-east-1.amazonaws.com;
docker tag buggy-dev-webapp:latest 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-dev-webapp:latest;
docker push 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-dev-webapp:latest;
elif [[ $1 = "local" ]]
then
docker build --build-arg APP_NAMESPACE=buggy --build-arg APP_ENVIRONMENT=dev --build-arg APP_ACCOUNT=575101084097 --build-arg APP_REGION=us-east-1 --build-arg API_URL=https://buggy.dev.api.networkearth.io --platform linux/amd64 -t buggy-local-webapp .
docker run -it -p 5001:5001 --env AWS_ACCESS_KEY_ID=$BUGGY_AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY=$BUGGY_AWS_SECRET_ACCESS_KEY --env AWS_DEFAULT_REGION=$BUGGY_AWS_DEFAULT_REGION buggy-local-webapp
else
echo "Please specify a valid environment..."
fi