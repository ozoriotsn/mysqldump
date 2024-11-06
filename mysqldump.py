#!/usr/local/bin/python3

from subprocess import Popen, PIPE
import os,time,sys,subprocess
from halo import Halo

HOST='localhost'
PORT='3306'
DB_USER='root'
DB_PASS='123'
DB_NAME='default'
LIMIT=1000000 # limite de registros por tabela

print("-- Script para exportar Databases --")

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install('halo')

def get_dump(database):
    filestamp = time.strftime('%Y-%m-%d-%I')
    spinner = Halo(text='Dumping %s' % database, spinner='dots')
    print("|| Starting Database export, exported to "+database,database+"_"+filestamp+".sql || ")
    spinner.start()

    mysqldump = os.popen("mysqldump --column-statistics=0  --opt --where='1 limit %s' -h %s -P %s -u %s -p%s %s > %s.sql" % (LIMIT,HOST,PORT,DB_USER,DB_PASS,database,database+"_"+filestamp))
    mysql = Popen(['mysql', '-u%s' % DB_USER, '-p%s' % DB_PASS, '-h%s' % HOST, '-P%s' % PORT, database], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = mysql.communicate(mysqldump.read())
    print(stdout)
    print(stderr)
    
    mysql.wait()
    mysqldump.close()
    mysql.stdout.close()
    mysql.stderr.close()
    spinner.stop()
    print("|| Finished Database export, exported to "+database,database+"_"+filestamp+".sql || ")

get_dump(DB_NAME)
