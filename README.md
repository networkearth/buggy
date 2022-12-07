# ewa-buggy-api
API for moving Earthwise Aware Buggy records to iNaturalist

```bash
cdk deploy --profile=deployer -c namespace=buggy -c environment=dev
```

In order for certificate validation to work you need to add a NS record to the base domain `networkearth.io` with the name servers of your subdomain. To do this create a new record on the `networkearth.io` hosted zone and set the subdomain. Then set the record type as NS. Go to your subdomain's hosted zone, grab the name servers from it's NS record and add them to the new NS record you are creating. Set the TTL to 172800 and then create the record, wait for it to sync, and then give a couple minutes for the certificate validation to finish.
