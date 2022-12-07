# ewa-buggy-api
API for moving Earthwise Aware Buggy records to iNaturalist

## Building the App
To build the app you'll need deployer credentials in your `~/.aws/credentials` file under the profile `deployer`. You'll need to build things out in a specific order:
1. `buckets`
2. Create the needed secrets (see `api` and `webapp` flask apps)
3. `api`
4. `webapp` and `push_to_inat`
5. `inaturalist_server`

And then if you want you can create the `dev_user` for running the `webapp` and `api` locally. Note that they depend on environment variables like the following to run locally:
```bash
export BUGGY_AWS_ACCESS_KEY_ID=<dev_user_access_key>
export BUGGY_AWS_SECRET_ACCESS_KEY=<dev_user_secret>
export BUGGY_AWS_DEFAULT_REGION=<dev_user_region>
```

Directions for each of these components can be found in the README.md files in their respectively subdirectories. s
