from bs4 import BeautifulSoup
import pymysql
from urllib2 import urlopen
from urllib2 import URLError
import time
import see

# Change these to suit your DB connection string
server = 'localhost'
username = 'root'
password = ''
database = 'results'
con = pymysql.connect(server, username, password, database)
cur = con.cursor()
# list to store USNs whose results are to be fetched
usns = []
done = {}
# students is the table that contains the pool of USNs to fetch results for
cur.execute('select usn,done from students')
for res in cur.fetchall():
    done[res[0]] = res[1]
    usns.append(res[0])

cone = True ;
while cone :
    for usn in usns:
		if done[usn] == 0 :
			try :
				print("Fetching results for USNs: " + str(usn))
				rows = []
				url = 'http://results.vtu.ac.in/results/result_page.php?usn=' + usn 
				soup = BeautifulSoup(urlopen(url),"html.parser")
				# Find the HTML table that contains the text "Subject"
				results_table = soup.find(text="Advanced Computer Architectures").find_parent("table")
				# Ectract all the content of <tr> tags
				results = results_table.find_all("tr")
				for row in results:
					rows.append([cell.get_text(strip=True) for cell in row.find_all("td")])
				for i in range(0, rows.__len__()):
					# All <tr>s with subject names contain an opening round bracket
					if rows[i] :
						code = rows[i][0] 
						subject = rows[i][1]
						internals = rows[i][2]
						externals = rows[i][3]
						total = rows[i][4]
						result = rows[i][5]
						u = usn
						print(usn, subject, internals, externals, total, result,code)
						try:
							cur.execute(
								"insert into marks(code,subject,internals,externals,total,result,usn) values (%s,%s,%s,%s,%s,%s,%s)", (code, subject, internals, externals, total, result,usn))
							cone = False ;
						except pymysql.err.IntegrityError:
							print("Error while inserting results of" + usn)
						continue
					else :
						print "empty"
					con.commit()
				try :	
					cur.execute ("""
							UPDATE students
							SET done=%s
							WHERE usn = %s
							""", (1,usn))
					con.commit()
					done[usn] = 1
					see.createbody(usn)
					
				except Exception as inst:
					print type(inst)
			except :
				print "Result not available" 
				cone = True 
				print "Sleeping"
				time.sleep(3)
		else :
			cone = False
