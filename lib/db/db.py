from os.path import isfile
from sqlite3 import connect
import psycopg
import os
from apscheduler.triggers.cron import CronTrigger

BUILD_PATH = "./data/db/build.sql"
HOST=os.getenv('POSTGRES_HOST')
DBNAME=os.getenv('POSTGRES_DB')
USER=os.getenv('POSTGRES_USER')
PASSWORD=os.getenv('POSTGRES_PASSWORD')


conn = psycopg.connect(host=HOST,dbname=DBNAME,user=USER,password=PASSWORD)
cur = conn.cursor()


def with_commit(func):
	def inner(*args, **kwargs):
		func(*args, **kwargs)
		commit()

	return inner


@with_commit
def build():
	if isfile(BUILD_PATH):
		scriptexec(BUILD_PATH)


def commit():
	conn.commit()


def autosave(sched):
	sched.add_job(commit, CronTrigger(second=0))


def close():
	conn.close()


def field(command, *values):
	cur.execute(command, tuple(values))

	if (fetch := cur.fetchone()) is not None:
		return fetch[0]


def record(command, *values):
	cur.execute(command, tuple(values))

	return cur.fetchone()


def records(command, *values):
	cur.execute(command, tuple(values))

	return cur.fetchall()


def column(command, *values):
	cur.execute(command, tuple(values))

	return [item[0] for item in cur.fetchall()]


def execute(command, *values):
	cur.execute(command, tuple(values))


def multiexec(command, valueset):
	cur.executemany(command, valueset)


def scriptexec(path):
	with open(path, "r", encoding="utf-8") as script:
		cur.execute(script.read())
