#!/bin/bash
if [[ $1 = "dev" ]]
then
docker build --build-arg APP_NAMESPACE=buggy --build-arg APP_ENVIRONMENT=dev --build-arg APP_ACCOUNT=575101084097 --build-arg APP_REGION=us-east-1 --platform linux/amd64 -t buggy-dev-api .
export AWS_PROFILE=deployer
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 575101084097.dkr.ecr.us-east-1.amazonaws.com;
docker tag buggy-dev-api:latest 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-dev-api:latest;
docker push 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-dev-api:latest;
elif [[ $1 = "local" ]]
then
docker build --build-arg APP_NAMESPACE=buggy --build-arg APP_ENVIRONMENT=dev --build-arg APP_ACCOUNT=575101084097 --build-arg APP_REGION=us-east-1 --platform linux/amd64 -t buggy-local-api .
docker run -it -p 5002:5002 --env AWS_ACCESS_KEY_ID=$BUGGY_AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY=$BUGGY_AWS_SECRET_ACCESS_KEY --env AWS_DEFAULT_REGION=$BUGGY_AWS_DEFAULT_REGION buggy-local-api
else
echo "Please specify a valid environment..."
fi