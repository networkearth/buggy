# Building the Job

The dev cdk deploy command:
```
cdk deploy --profile=deployer -c namespace=buggy -c environment=dev
```

Note that for the following to work you'll have needed to setup the compute environment and job queue manually in the console. Check the `batch_job/stack.py` file to see the appropriate names for these. The compute environment should have a limit of 1 job at a time in order to ensure we rate limit the pushes to iNaturalist. 

1. Create the role by entering the `role` directory and running your cdk deploy command.
2. Create the container registry and batch job definition by entering the `batch_job` directory and running your cdk command.
3. Build and push the container using `./build.sh dev`

