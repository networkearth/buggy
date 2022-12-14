# iNaturalist Development Server

## Setting up the EC2
1. Create a key pair called `inaturalist`
2. Build the EC2 by going into the `stack` folder and running `cdk deploy --profile deployer`
3. You're going to want to setup an elastic ip so you can shut down the instance without the ip switching
4. SSH into the EC2
5. Setup GIT 
6. Pull this repository into the EC2
7. Install docker https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 (note that you want to follow the instructions to not need to use `sudo` as well https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)
8. Install docker-compose https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

## Building iNaturalist

### Building the Webapp and Services

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
  host: 44.212.148.112
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
export PGHOST=44.212.148.112
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

Update `config/config.yml` to replace all instances of `localhost` with `44.212.148.112`.

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
rails r "Site.create( name: 'iNaturalist', url: 'http://44.212.148.112:3000' )"
rake inaturalist:generate_translations_js
rails r tools/load_iconic_taxa.rb
```

You'll get lots of translation warning messages, but no need to worry.

Add the following to the end of `config/environments/development.rb`:
```bash
config.hosts << "44.212.148.112"
```
Note that you'll need to grab the appropriate elastic ip from the aws console

Test it out with
```bash
rails s -b 0.0.0.0
```

Okay before we leave here let's just go ahead and create a fake user or two as well as a fake oauth application:

Create a `tools/create_users_and_app.rb` file:
```ruby
opts = {
    :login => 'john',
    :email => 'john@example.com',
    :password => 'password123',
    :password_confirmation => 'password123'
}
u = User.new(opts)
u.save
u

opts = {
    :login => 'jill',
    :email => 'jill@example.com',
    :password => 'password123',
    :password_confirmation => 'password123'
}
u = User.new(opts)
u.save
u

opts = {
    :name => 'buggy',
    :redirect_uri => 'http://localhost:5000'
}
app = OauthApplication.new(opts)
app.save
app
```

and then run it with: 
```bash
chmod 777 tools/create_users_and_app.rb
rails r tools/create_users_and_app.rb
```

Now go ahead and shut down the rails app and then before exiting the container let's save all that work we did:
```bash
docker commit inaturalist_webapp_base_container inaturalist_webapp_updated/latest
```

Most of what we just did to the supporting containers shows up in their respective data volumes. So if we're going to keep those around we need to tar those up and commit them to git. Specifically the volumes are in the `~/inaturalist_volumes` directory. So once you've shut down the services (so nothing's being updated while you tar things up) you can go ahead and run:

```bash
cd ~/
tar -czf inaturalist_volumes.tar.gz inaturalist_volumes
```

Then move the tar into this repository and commit it. 

We've got a container with everything in it, but now we need to build an image that will actuall start our app for us. From within the `webapp` directory of `dockerized_inaturalist` run:

```bash
docker build -t inaturalist_webapp/latest -f DockerfileFinal .
```

You can test the image with:

```bash
docker run --add-host=host.docker.internal:host-gateway -p 3000:3000 inaturalist_webapp/latest
```

### Building the API
From within the `api` directory run:

```bash
docker build -t inaturalist_api_base/latest -f DockerfileBase .
```

Start up the base container with:

```bash
docker run --rm --add-host=host.docker.internal:host-gateway --name inaturalist_api_base_container -p 4000:4000 -it inaturalist_api_base/latest
```

Update the hosts in `config.js` to point to `44.212.148.112` for all the services and the webapp. Also change the DB password to be `password` and user to be `username`. You'll also need to add an `http://` in front of the hostname for elasticsearch. 

Setup Node
```bash
nvm install
npm install
```

You can try it out by running:
```bash
node app.js
```

Now before exiting from the container let's save our work

```bash
docker commit inaturalist_api_base_container inaturalist_api_updated/latest
```

Okay now we can build and try out the real image:

```bash
docker build -t inaturalist_api/latest -f DockerfileFinal .
```

You can test the image with:

```bash
docker run --add-host=host.docker.internal:host-gateway -p 4000:4000 inaturalist_api/latest
```