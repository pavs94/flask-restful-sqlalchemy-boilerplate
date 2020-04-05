import pandas as pd
import time
from flask import json
from models import *

def mk_session(fun):
	def wrapper(*args, **kwargs):
		s = session()
		kwargs['session'] = s
		try:
			res = fun(*args, **kwargs)
		except Exception as e:
			s.rollback()
			s.close()
			raise e

		s.close()
		return res
	wrapper.__name__ = fun.__name__
	return wrapper

def retry_db(exceptions, n_retries=3, ival=1):
	def decorator(fun):
		@wraps(fun)
		def wrapper(*args, **kwargs):
			exception_logged = False
			for r in range(n_retries):
				try:
					return fun(*args, **kwargs)
				except exceptions as e:
					if not exception_logged:
						print(e)
						exception_logged = True
					else:
						print("Retry #{r} after receiving exception.")
					time.sleep(ival)
			return fun(*args, **kwargs)
		return wrapper
	return decorator

#Get Users from the database
@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def dbGetUser(email, session=None):
    checkUser = session.query(Users).with_entities(Users.idusers, Users.email, Users.username).filter(Users.email==email).statement
    df=pd.read_sql(checkUser,engine)
    return df.to_json(orient="records")




