#!/usr/bin/python

import MySQLdb
import os
import shutil

FOLDER = "backup"
IGNORE_DATABASES = ["information_schema", "performance_schema", "pi_backup", "priceinfocenter_test"]

BUCKET = "gendis-zuelch"
BUCKET_FOLDER = "patlocal"

if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)
os.makedirs(FOLDER)

db=MySQLdb.connect()
c = db.cursor()
c.execute("""SHOW DATABASES""")

for row in c.fetchall():
        name = row[0]
        if name in IGNORE_DATABASES:
                continue
        cmd = "mysqldump --events {0} > {1}/{2}.sql".format(name, FOLDER, name)
        os.system(cmd)

os.system("tar cvfz `hostname`_`date +%Y%m%d`.tar.gz backup")
os.system("s3cmd put `hostname`_`date +%Y%m%d`.tar.gz s3://gendis-zuelch/patlocal/`date +%Y%m%d`_`ho$
os.system(""" /usr/local/lib/backup/expire.sh "gendis-zuelch/patlocal" "30 Days" """)
