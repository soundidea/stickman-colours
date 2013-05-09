import sqlite3 as sql
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
db = sql.connect('colorsurvey.db')
with db:
	db.row_factory = sql.Row
	cur = db.cursor();

	print """
/* Each row contains a colour. The fields are as follows:
 *   colours[n][0] - Name 
 *   colours[n][1] - Count (number of answers) 
 *   colours[n][2] - Red 0-255
 *   colours[n][3] - Green 0-255
 *   colours[n][4] - Blue 0-255
 *   colours[n][5] - CIELAB L*
 *   colours[n][6] - CIELAB a*
 *   colours[n][7] - CIELAB b*
 *   colours[n][8] - Variance
 */
var colours = ["""

	cur.execute("SELECT * FROM averages ORDER BY count DESC LIMIT 1000;")
	while True:
		row = cur.fetchone()
		if row == None:
			break
		print ("["
			+ "\"" + row["name"] + "\","
			+ str(row["count"]) + ","
			+ str(int(round(row["rgb_R"]))) + ","
			+ str(int(round(row["rgb_G"]))) + ","
			+ str(int(round(row["rgb_B"]))) + ","
			+ "{0:.3f}".format(row["clab_L"]) + ","
			+ "{0:.3f}".format(row["clab_a"]) + ","
			+ "{0:.3f}".format(row["clab_b"]) + ","
			+ "{0:.3f}".format(row["variance"])
			+ "],")
	print "];"
