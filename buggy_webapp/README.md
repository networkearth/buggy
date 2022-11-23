```bash
docker build --platform linux/amd64 -t buggy-webapp .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 575101084097.dkr.ecr.us-east-1.amazonaws.com;
docker tag buggy-webapp:latest 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-webapp:latest;
docker push 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-webapp:latest;
```

```bash
docker build --platform linux/amd64 --build-arg KOBO_USERNAME=$KOBO_USERNAME --build-arg KOBO_PASSWORD=$KOBO_PASSWORD -t buggy-webapp .

docker run -p 5001:5001 -it buggy-webapp
```
