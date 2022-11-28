import click

from subprocess import Popen, PIPE, STDOUT

@click.command()
@click.option('-c', '--container', required=True, help='name of the container to run')
@click.option('-r', '--region', required=True, help='the aws region')
def main(container, region):
    
    email = 'john@example.com'
    bucket = 'buggy-job-bucket'
    api_url = 'http://buggy-api-service-791649285.us-east-1.elb.amazonaws.com'
    inat_api = 'http://44.212.148.112:4000/v1'
    inat_webapp = 'http://44.212.148.112:3000'
    cmd = f'docker run {container} -e {email} -b {bucket} -a {api_url} -ia {inat_api} -iw {inat_webapp} -r {region}'
    print('running:', cmd)
    with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as process:
        print(process.stdout.read().decode('utf-8'))

if __name__ == '__main__':
    main()