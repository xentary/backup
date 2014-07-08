#!/usr/bin/python

import MySQLdb
import os
import shutil

FOLDER = "backup"
IGNORE_DATABASES = ["information_schema", "performance_schema", "pi_backup", "priceinfocenter_test"]
IGNORE_TABLES = []

BUCKET = "gendis-zuelch"
BUCKET_FOLDER = "patlocal"

if os.path.exists(FOLDER):
	shutil.rmtree(FOLDER)
os.makedirs(FOLDER)

db=MySQLdb.connect()
c = db.cursor()
c.execute("""SHOW DATABASES""")

for row in c.fetchall():
	dbname = row[0]
	if dbname in IGNORE_DATABASES:
		continue

	tc = db.cursor()
	tc.execute("USE {0}".format(dbname))
	tc.execute("SHOW TABLES")
	for table in tc.fetchall():
		table = table[0]

		if table in IGNORE_TABLES:
			continue

		dbfolder = "{0}/{1}".format(FOLDER, dbname)
		if not os.path.exists(dbfolder):
			os.makedirs(dbfolder)

		cmd = """mysqldump {3} --events {0} '{2}' > {1}/{2}.sql""".format(dbname, dbfolder, table, DB_PW)
		os.system(cmd)
	tc.close()

os.system("tar cvfz `hostname`_`date +%Y%m%d`.tar.gz backup")
os.system("s3cmd put `hostname`_`date +%Y%m%d`.tar.gz s3://gendis-zuelch/patlocal/`date +%Y%m%d`_`hostname`.tar.gz")
os.system(""" /usr/local/lib/backup/expire.sh "gendis-zuelch/patlocal" "30 Days" """)
