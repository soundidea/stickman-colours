import sqlite3 as sql
import colour_convert as c
import sys

db = sql.connect('colorsurvey.db')
with db:
	db.row_factory = sql.Row
	write_cur = db.cursor();
	write_cur.executescript("""
		DROP TABLE IF EXISTS conv_ans;
		CREATE TABLE conv_ans(
			id INT, name TEXT,
			rgb_r REAL, rgb_g REAL, rgb_b REAL,
			clab_l REAL, clab_a REAL, clab_b REAL);
		CREATE INDEX name ON conv_ans(name);""")
	read_cur = db.cursor();
	read_cur.execute("SELECT count(*) as C FROM answers;")
	count = str(read_cur.fetchone()["C"])
	read_cur.execute("SELECT * FROM answers;")
	i = 1
	while True:
		row = read_cur.fetchone()
		if row == None:
			break
		name = row["colorname"] \
			.strip() \
			.replace("  ", " ") \
			.replace('"', "") \
			.replace("!", "") \
			.replace("?", "") \
			.replace(".", "") \
			.replace(",", "")
		if (i % 100 == 1) or (i == count):
			print "\r\033[2K[" + str(i) + "/" + count + "]",
			sys.stdout.flush()
		i += 1
		(id, name, R, G, B) = (row["id"], name, row["r"], row["g"], row["b"])
		(X, Y, Z) = c.rgb_2_xyz(R, G, B)
		(clab_L, clab_a, clab_b) = c.xyz_2_cielab(X, Y, Z)
		write_cur.execute(
			"INSERT INTO conv_ans VALUES(?,?,?,?,?,?,?,?);",
			(id, name, R, G, B, clab_L, clab_a, clab_b))
