import mysql.connector
from ProjectConfig import *
from pii import get_hashables, random_algo
import hashlib
import sys

cnx=mysql.connector.connect(host=HOST,database=DATABASE,user=DBUSER,password=DBPASSWORD)
cursor = cnx.cursor()
if(sys.argv[1]):
	to_hash, to_numerical = get_hashables(str(sys.argv[1]))
else:
	print 'Please enter database name whose yml is present.'
	exit(1)

try:
	for tables in to_hash:
		for column in to_hash[tables]:
			update_statement = 'update '+tables+' set ' + column + '=' + 'sha1('+column+')'
			cursor.execute(update_statement)

	for tables in to_numerical:
		for column in to_numerical[tables]:
			update_statement = 'update '+tables+' set ' + column + '=' + column + '*' + str(RANDOM_MULTIPLIER) + '+' + str(RANDOM_ADD)
			cursor.execute(update_statement)
except:
	print 'Please check database name whose yml is present.'
	exit(1)
cnx.commit()
exit(0)
