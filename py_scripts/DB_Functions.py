import pymysql

__conn = pymysql.connect(host='localhost', database='acr_dat', user='root', password='')
__cursor = __conn.cursor()

def insert_user(user_id, user_elo):
	__cursor.execute("INSERT INTO User_Scores (user_id, elo_global) VALUES ({}, {})".format(user_id, user_elo))
	__conn.commit()

def user_submissions(user_id):
	__cursor.execute("SELECT id, problem_id, status, submissionDate FROM submission WHERE user_id={} ORDER BY submissionDate DESC".format(user_id))
	return __cursor.fetchall()

def problem_list():
	__cursor.execute("SELECT internalId, title, totalDistinctUsers FROM problem ORDER BY internalId ASC")
	return __cursor.fetchall()

def user_list():
	__cursor.execute("""SELECT user_id, COUNT(DISTINCT(problem_id)), SUM(CASE 
							WHEN status = 'AC' THEN 1 
							WHEN status = 'PE' THEN 1 
							ELSE 0 END) FROM submission 
							GROUP BY user_id 
							ORDER BY user_id ASC""")
	return __cursor.fetchall()