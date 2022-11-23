```bash
docker build --platform linux/amd64 -t buggy-api .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 575101084097.dkr.ecr.us-east-1.amazonaws.com;
docker tag buggy-api:latest 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-api:latest;
docker push 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-api:latest;
```

```bash
build --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION --platform linux/amd64 -t buggy-api .
docker run -it -p 5000:5000 buggy-api
```
