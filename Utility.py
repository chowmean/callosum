import boto
import boto.s3.connection
import csv
import os

class awsS3:
	def getfile(self,access_key,secret_key,database):
		print "Getting file from s3"
		conn = boto.connect_s3(
	        aws_access_key_id = access_key,
	        aws_secret_access_key = secret_key,
	        is_secure=False
	        )
		bucket = conn.get_bucket("asdtasdasipoca")
		keys_list=[]
		marker = None
		while True:
			print "next itter"
			keys = bucket.get_all_keys(prefix="bckp_"+database,marker=marker)
			last_key = None

			for k in keys:
			    keys_list.append(k)
			    last_key = k.name

			if not keys.is_truncated:
			    break
			marker = last_key
		return keys_list

	def splitFile(self,filename):
		divisor=10000
		outfile=None
		outfileno = 1
		with open(filename, 'r') as infile:
		    for index, row in enumerate(csv.reader(infile)):
		        if index % divisor == 0:
		            if outfile is not None:
		                outfile.close()
		            if not os.path.exists('split_file'):
		    			os.makedirs('split_file')
		            outfilename = 'split_file/'+filename.split('.')[0]+'__big-{}.csv'.format(outfileno)
		            outfile = open(outfilename, 'w')
		            outfileno += 1
		            writer = csv.writer(outfile)
		        writer.writerow(row)

 	def createQuery(self):
 		a=open('create.sql','r')
		b=open('created.sql','w')
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
		b.write(statement);
		a.close()
		b.close()
		return statement

	def deleteAllTable(self,tablesArray):
		string=""
		with open("delete.sql",'w') as f:
			for table in tablesArray:
				string=string+"drop table " + table + ";";
			f.write(string)
