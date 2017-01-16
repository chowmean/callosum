import boto.ec2
from ProjectConfig import *
from subprocess import call,Popen
from fabric.api import *

conn = boto.ec2.connect_to_region("us-west-2",
        aws_access_key_id=AWSKEY,
        aws_secret_access_key=AWSSECRET)

conn.run_instances(
        AMIID,
        key_name='myKey',
        instance_type='t2.medium',
        security_groups=['your-security-group-here'])

instance = conn.instances[0]

while instance.state != 'running':
        print '...instance is %s' % instance.state
        time.sleep(10)
        instance.update()


runProcess=Popen('fab run', shell=True)
