import boto.rds
import boto.ec2
import mysql.connector
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
    else:
        fileset = FABRIC_TABLES
    a = Utility.awsS3()
    access_key = AWSKEY
    secret_key = AWSSECRET
    starttime=time.time()
    filelist=a.getfile(access_key,secret_key,database)
    filelist = sorted(filelist, key=lambda k: k.last_modified)
    filelist.reverse()
    Iterated=[]
    echo blahblahblahblah >> OUTFILE
    for fileitem in fileset:
    	for file in filelist:
    		if  file.name.split('/')[1].split('$')[0]==fileitem and fileitem not in Iterated:
    			Iterated.append(fileitem)
    			print file.name
    			file.get_contents_to_filename(file.name.split('/')[1].split('$')[0]+'.csv')
    			temp_process1=Popen('mysqlimport --local -u '+LOCAL_USER+' -p'+LOCAL_PASSWORD+' --fields-terminated-by=, '+database+' '+file.name.split('/')[1].split('$')[0]+'.csv  >> process.log', shell=True)
    			temp_process1.wait()
	                remove_csv_process=Popen('rm '+file.name.split('/')[1].split('$')[0]+'.csv >> process.log', shell=True)
        	        remove_csv_process.wait()
               		temp_process2=Popen('mysqldump -u '+LOCAL_USER+' -p'+LOCAL_PASSWORD+' '+database+' '+ file.name.split('/')[1].split('$')[0] +' > table.sql >> process.log', shell=True)
    	       		temp_process2.wait()
           		temp_process3=Popen('mysql -u '+DBUSER+' -h '+HOST+' -p'+DBPASSWORD+' '+database+' < table.sql >> process.log', shell=True)
           		temp_process3.wait()


def destroy_instance():
    temp_process=Popen('shutdown -h now', shell=True)


if __name__ == "__main__":
    startlog=Popen('echo Starting >> process.log', shell=True)
    startlog.wait()
    do_work('feedback')
    do_work('fabric')
    destroy_instance()
