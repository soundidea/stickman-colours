import sqlite3 as sql
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
db = sql.connect('colorsurvey.db')
with db:
	db.row_factory = sql.Row
	cur = db.cursor();

	print "var colours = ["

	cur.execute("SELECT * FROM averages ORDER BY count DESC LIMIT 1000;")
	while True:
		row = cur.fetchone()
		if row == None:
			break
		print ("{"
			+ "\"name\":\"" + row["name"] + "\","
			+ "\"count\":" + str(row["count"]) + ","
			+ "\"rgb\":["
				+ str(int(round(row["rgb_R"]))) + ","
				+ str(int(round(row["rgb_G"]))) + ","
				+ str(int(round(row["rgb_B"]))) + "],"
			+ "\"cielab\":["
				+ "{0:.3f}".format(row["clab_L"]) + ","
				+ "{0:.3f}".format(row["clab_a"]) + ","
				+ "{0:.3f}".format(row["clab_b"]) + "],"
			+ "\"var\":" + "{0:.3f}".format(row["variance"])
			+ "},")
	print "];"
