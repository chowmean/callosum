import boto.ec2
from ProjectConfig import *
from subprocess import call,Popen
from fabric.api import *

conn = boto.ec2.connect_to_region("ap-southeast-1",
        aws_access_key_id=AWSKEY,
        aws_secret_access_key=AWSSECRET)

conn.run_instances(
    image_id=AMIID,
    key_name=KEYNAME,
    security_group_ids=[SECURITY_GRP],
    subnet_id=SUBNET_ID,
    )

instance = conn.instances[0]

while instance.state != 'running':
        print '...instance is %s' % instance.state
        time.sleep(10)
        instance.update()

instance.add_tag("Name",TAGNAME)
print instance.public_dns_name


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


#createQuery('feedback');
#createQuery('fabric');
runProcess=Popen('fab -i '+KEYNAME+' -h '+instance.public_dns_name+' get_project', shell=True)
Popen(["scp","-i",KEYNAME, "ProjectConfig.py", "ubuntu@"+instance.public_dns_name+":callosum/ProjectConfig.py"])
Popen(["scp","-i",KEYNAME, "created_fabric.sql", "ubuntu@"+instance.public_dns_name+":callosum/created.sql"])
Popen(["scp","-i",KEYNAME, "delete_fabric.sql", "ubuntu@"+instance.public_dns_name+":callosum/delete.sql"])
Popen(["scp","-i",KEYNAME, "created_feedback.sql", "ubuntu@"+instance.public_dns_name+":callosum/created.sql"])
Popen(["scp","-i",KEYNAME, "delete_feedback.sql", "ubuntu@"+instance.public_dns_name+":callosum/delete.sql"])
runProcess=Popen('fab -i '+KEYNAME+' -h '+instance.public_dns_name+' run', shell=True)
