from setuptools import setup, find_packages

setup(
    name='buggy_deployer',
    version='0.0.1',
    author_email='marcelsanders96@gmail.com',
    description='Automation',
    packages=find_packages(include=['buggy_deployer', 'buggy_deployer*']),
    install_requires=[
        'click',
        'aws-cdk-lib==2.44.0',
        'aws-cdk.aws-batch-alpha==2.44.0a0'
    ],
    entry_points={
        'console_scripts': [
            'synth_batch_job = buggy_deployer.jobs.app:main',
            'deploy_batch_job = buggy_deployer.jobs.deploy:main',
        ]
    }
)