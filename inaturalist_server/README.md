# iNaturalist Development Server

## Setting up the EC2
1. Create a key pair called `inaturalist`
2. Build the EC2 by going into the `stack` folder and running `cdk deploy --profile deployer`
3. SSH into the EC2
4. Setup GIT 
5. Pull this repository into the EC2
6. Install docker https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 (note that you want to follow the instructions to not need to use `sudo` as well https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)
7. Install docker-compose https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

## Building iNaturalist

### Building the Webapp

Start by building the base image we'll use for the webapp. So go to the `webapp` folder and run:

```bash
docker build -t inaturalist_webapp_base/latest -f DockerfileBase .
```

iNaturalist depends on a few other applications for which we'll be making images as well. To get the base images up and running for modification go to the `supporting` directory of `dockerized_inaturalist` and run the following:
```bash
docker-compose build --parallel es memcached redis pg
docker-compose up es memcached redis pg
```

(Note that you'll want these to be fresh so good idea to just run a `docker-compose rm` to check)

You'll need to wait until the services are up and running.

Note that as iNaturalist gets setup it also sets up the database and elasticsearch, so you'll need to set these things up concurrently.

```bash
docker run --rm --add-host=host.docker.internal:host-gateway --name inaturalist_webapp_base_container -p 3000:3000 -it inaturalist_webapp_base/latest
```

Write the following to `config/database.yml`

```yaml
login: &login
  host: host.docker.internal
  encoding: utf8
  adapter: postgis
  template: template_postgis
  username: username
  password: password

development:
  <<: *login
  database: inaturalist_development

test:
  <<: *login
  database: inaturalist_test

production:
  <<: *login
  database: inaturalist_production
```

Export the following environment variables so you can connect to the database with `psql`:
```bash
export PGHOST=host.docker.internal
export PGUSER=username
export PGPASSWORD=password
```

Setup the database with:
```bash
ruby bin/setup
```

If you see some errors about things already existing, that's fine as the service already has some things setup.

```bash
== Creating Template Database ==
createdb: error: database creation failed: ERROR:  database "template_postgis" already exists
bin/setup:37:in `system': Command failed with exit 1: createdb (RuntimeError)
        from bin/setup:37:in `block in <main>'
        from /root/.rbenv/versions/3.0.4/lib/ruby/3.0.0/fileutils.rb:139:in `chdir'
        from /root/.rbenv/versions/3.0.4/lib/ruby/3.0.0/fileutils.rb:139:in `cd'
        from bin/setup:10:in `<main>'
```

Then using `psql` run the following:
```psql
CREATE database inaturalist_development; 
CREATE database inaturalist_test;
```

Back in `bash` execute the following to setup the schemas:
```bash
rake db:schema:load
```

Update `config/config.yml` to replace all instances of `localhost` with `host.docker.internal`.

then run
```bash
rake es:rebuild
```

Setup node:
```bash
nvm install 
npm install
npm run webpack 
```

Now let's seed some data in the site
```bash
rails r "Site.create( name: 'iNaturalist', url: 'http://localhost:3000' )"
rake inaturalist:generate_translations_js
rails r tools/load_iconic_taxa.rb
```

You'll get lots of translation warning messages, but no need to worry.

Add the following to the end of `config/environments/development.rb`:
```bash
config.hosts << "host.docker.internal"
config.hosts << "ec2-3-83-47-52.compute-1.amazonaws.com"
```
Note that you'll need to grab the appropriate hostname from the aws console