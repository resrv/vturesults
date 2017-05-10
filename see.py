import pymysql
import sendsms
server = 'localhost'
username = 'root'
password = ''
database = 'results'
con = pymysql.connect(server, username, password, database)
cur = con.cursor()
def createbody(usn) :
	query = "select code,total from marks where usn = '%s' " % usn
	cur.execute(query)
	r = cur.fetchall()
	body = '' 
	for res in r:
		 body += res[0] +'\t'+str(res[1])+'\n'
	sendsms.send(body)
