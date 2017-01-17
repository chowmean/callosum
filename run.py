import boto.rds
import boto.ec2
import csv
import sys
import Utility
import os
import time
from ProjectConfig import *
from os import listdir, rmdir, remove
from subprocess import call,Popen

def do_work(database):
    if(database=="feedback"):
        fileset = FEEDBACK_TABLES
        q=Popen('mysql -u '+LOCAL_USER+' '+database+' < created_feedback.sql >> process.log', shell=True)
        q.wait()
    else:
        fileset = FABRIC_TABLES
        q=Popen('mysql -u '+LOCAL_USER+' '+database+' < created_fabric.sql >> process.log', shell=True)
        q.wait()
    a = Utility.awsS3()
    access_key = AWSKEY
    secret_key = AWSSECRET
    starttime=time.time()
    filelist=a.getfile(access_key,secret_key,database)
    filelist = sorted(filelist, key=lambda k: k.last_modified)
    filelist.reverse()
    Iterated=[]
    for fileitem in fileset:
    	for file in filelist:
    		if  file.name.split('/')[1].split('$')[0]==fileitem and fileitem not in Iterated:
    			Iterated.append(fileitem)
    			print file.name
    			file.get_contents_to_filename(file.name.split('/')[1].split('$')[0]+'.csv')
    			temp_process1=Popen('mysqlimport --local -u '+LOCAL_USER+'  --fields-terminated-by=, '+database+' '+file.name.split('/')[1].split('$')[0]+'.csv  >> process.log', shell=True)
    			temp_process1.wait()
	                remove_csv_process=Popen('rm '+file.name.split('/')[1].split('$')[0]+'.csv >> process.log', shell=True)
        	        remove_csv_process.wait()
               		temp_process2=Popen('mysqldump -u '+LOCAL_USER+' '+database+' '+ file.name.split('/')[1].split('$')[0] +' > table.sql >> process.log', shell=True)
    	       		temp_process2.wait()
           		temp_process3=Popen('mysql -u '+DBUSER+' -h '+HOST+' -p'+DBPASSWORD+' '+database+' < table.sql >> process.log', shell=True)
           		temp_process3.wait()
                	break;


if __name__ == "__main__":
    startlog=Popen('echo Starting >> process.log', shell=True)
    startlog.wait()
    do_work('feedback')
    #do_work('fabric')
    conn = boto.ec2.connect_to_region("ap-southeast-1",
            aws_access_key_id=AWSKEYEC,
            aws_secret_access_key=AWSSECRETEC)


    reservations = conn.get_all_instances(filters={"tag:Name" : TAGNAME})
    for reservation in reservations:
        if reservation.instances[0].state=='running':
            print reservation.instances[0].instance_type
            print reservation.instances[0].id
            a=raw_input("Terminating..")
            conn.terminate_instances(reservation.instances[0].id)
