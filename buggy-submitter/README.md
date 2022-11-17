```bash
docker build --platform linux/amd64 -t buggy-submitter .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 575101084097.dkr.ecr.us-east-1.amazonaws.com;
docker tag buggy-submitter:latest 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-submitter:latest;
docker push 575101084097.dkr.ecr.us-east-1.amazonaws.com/buggy-submitter:latest;
```
