# Building the WebApp

The dev cdk deploy command:
```
cdk deploy --profile=deployer -c namespace=buggy -c environment=dev
```

1. Create the container registry by entering the `stacks/container` directory and running your cdk deploy command.
2. Create the role by entering the `stacks/role` directory and running your cdk deploy command.
3. Build out and deploy your container by running `./build.sh dev` (you can try out the container locally by running `./build.sh local`)
4. Create the full stack by entering the `stacks/service` directory and running your cdk deploy command.
5. When the stack deploy hits the certificate building stage, you're going to need to update the name server records for your base domain in order to have DNS validation work correctly for your certificate. To do this open up the hosted zone of your base domain (`networkearth.io` for example) and create a new record. Add your subdomain (`buggy.dev.api.` for example) and set the record type to NS. Then open up your hosted zone for the subdomain (`buggy.dev.api.networkearth.io` for example) and go to the NS record for it. Copy the name servers to the new record you are creating, set the TTL to 172800 and then create the record. Wait for it to sync and then a few minutes later your certificate should succeed in validation and get issued. 