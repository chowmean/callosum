import boto.ec2
from ProjectConfig import *
from subprocess import call,Popen
from fabric.api import *
import time

conn = boto.ec2.connect_to_region("ap-southeast-1",
        aws_access_key_id=AWSKEYEC,
        aws_secret_access_key=AWSSECRETEC)

print conn
conn=conn.run_instances(
    image_id=AMIID,
    key_name=KEYPAIR,
    subnet_id=SUBNET_ID,
    instance_type="t2.small",
    security_group_ids=SECURITY_GRP
    )

instance = conn.instances[0]

while instance.state != 'running':
        print '...instance is %s' % instance.state
        time.sleep(10)
        instance.update()

instance.add_tag("Name",TAGNAME)
print instance.public_dns_name

public_dns_name=instance.public_dns_name

def createQuery(table):
 	a=open('create_'+table+'.sql','r')
	b=open('created_'+table+'.sql','w')
	statement=""

	with open("create.sql") as f:
		arr=[word for line in f for word in line.split()]
		inp=False
		for word in arr:
		    	if word == "CREATE":
		    		inp=True
		    	if(inp==True):
		    		statement=statement+word
		    		statement=statement+" "
		    	if(word==");"):
		    	 	inp=False
	statement=statement.replace('character varying','varchar')
	statement=statement.replace('character','varchar')
	statement=statement.replace('timestamp without time zone','datetime')
	statement=statement.replace('"timestamp"','timestamp')
	statement=statement.replace('32768','1000')
	b.write(statement);
	a.close()
	b.close()
	return statement

time.sleep(120)
#createQuery('feedback');
#createQuery('fabric');
runProcess=Popen('echo "yes\n"| fab -i '+KEYNAME+' -H '+public_dns_name+' get_project > process.log', shell=True)
runProcess.wait()
p=Popen(["scp","-i",KEYNAME,"-oStrictHostKeyChecking=no", "ProjectConfig.py", "ubuntu@"+public_dns_name+":callosum/ProjectConfig.py"])
p.wait()
p=Popen(["scp","-i",KEYNAME,"-oStrictHostKeyChecking=no", "created_fabric.sql", "ubuntu@"+public_dns_name+":callosum/created_fabric.sql"])
p.wait()
p=Popen(["scp","-i",KEYNAME,"-oStrictHostKeyChecking=no", "delete_fabric.sql", "ubuntu@"+public_dns_name+":callosum/delete_fabric.sql"])
p.wait()
p=Popen(["scp","-i",KEYNAME,"-oStrictHostKeyChecking=no", "created_feedback.sql", "ubuntu@"+public_dns_name+":callosum/created_feedback.sql"])
p.wait()
p=Popen(["scp","-i",KEYNAME,"-oStrictHostKeyChecking=no", "delete_feedback.sql", "ubuntu@"+public_dns_name+":callosum/delete_feedback.sql"])
p.wait()
runProcess=Popen('fab -i '+KEYNAME+' -H '+public_dns_name+' runn >> process.log', shell=True)
runProcess.wait()
