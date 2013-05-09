import sqlite3 as sql
import colour_convert as c
import sys

db = sql.connect('colorsurvey.db')
with db:
	db.row_factory = sql.Row
	cur = db.cursor();
	cur.executescript("""
		DROP TABLE IF EXISTS averages;
		CREATE TABLE averages(
			name TEXT,
			count INT,
			rgb_R REAL,
			rgb_G REAL,
			rgb_B REAL,
			clab_L REAL,
			clab_a REAL,
			clab_b REAL,
			variance REAL);""")

	# Get all unique colour names
	print "Fetching colour names...",
	sys.stdout.flush()
	cur.execute("SELECT DISTINCT name FROM conv_ans;")
	colour_names = cur.fetchall()
	print "done"

	count = len(colour_names)
	i = 1;

	for nq in colour_names:
		name = nq["name"]
		if (i % 100 == 1) or (i == count):
			print "\r\033[2KProcessing colours... [" + str(i) + "/" + str(count) + "]",
			sys.stdout.flush()
		i += 1

		# First grab all the results with this colour name
		cur.execute(
			"""CREATE TEMP TABLE colour_t AS
				SELECT clab_l as L, clab_a as a, clab_b as b
				FROM conv_ans
				WHERE name = '""" + name.replace("'", "''") + "';")

		# Calculate the average and variance all at once
		cur.execute(
			"""SELECT count(*) as cnt, a.L AS L, a.a AS a, a.b AS b,
				AVG((c.L - a.L) * (c.L - a.L)
					+ (c.a - a.a) * (c.a - a.a)
					+ (c.b - a.b) * (c.b - a.b)) AS v
				FROM colour_t AS c,
					(SELECT AVG(L) AS L, AVG(a) AS a, AVG(b) AS b
						FROM colour_t) as a;""")
		result = cur.fetchone()
		cur.execute("DROP TABLE colour_t;")

		(X,Y,Z) = c.cielab_2_xyz(result["L"], result["a"], result["b"])
		(R,G,B) = c.xyz_2_rgb(X,Y,Z)

		# Store the result, but only if it has some variance
		if result["v"] > 0:
			cur.execute("INSERT INTO averages VALUES(?,?,?,?,?,?,?,?,?);",
				(name, result["cnt"], R, G, B, result["L"], result["a"],
				result["b"], result["v"]))

	# Finally, I believe that the greatest variance from the most-popular 50 colours
	# will be the largest I need to care about, so I delete all colours with a
	# greater variance. This remove entries like 'I don't know' or racial slurs,
	# which are essentially spam because they're associated with too many different
	# colours.
	print "\nPruning spam...",
	sys.stdout.flush()
	cur.execute("""
		DELETE FROM averages
		WHERE variance > (SELECT MAX(variance)
				  FROM (SELECT *
					FROM averages
					ORDER BY count DESC
					LIMIT 50));""")
	print "done"
