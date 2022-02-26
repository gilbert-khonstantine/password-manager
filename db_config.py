from sqlalchemy import create_engine, select
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
import os
from dotenv import load_dotenv

load_dotenv()
class DatabaseConfig:
	def __init__(self):
		print(os.getenv('DB_URI'))
		self.db_uri = os.getenv('DB_URI')
		self.engine = create_engine(self.db_uri)
		self.meta = MetaData(self.engine)

	def create_table(self):
		self.user = Table('User', self.meta,
		           Column('id',Integer, primary_key=True, autoincrement = True),
		           Column('account_name',String),
		           Column('master_password',String))

		self.password = Table('Password', self.meta,
		           Column('id',Integer, primary_key=True, auto_increment = True),
		           Column('account',String),
		           Column('platform',String),
		           Column('username',String),
		           Column('email',String),
		           Column('password',String))
		self.meta.create_all()

	def getUserTable(self):
		return self.user

	def getPasswordTable(self):
		return self.password

	def getConnection(self):
		return self.engine.connect()

# # runner code
# dbConfig : DatabaseConfig = DatabaseConfig()
# dbConfig.create_table()
# dbConfig.password
# user_table : Table = dbConfig.getUserTable()
# pwd_table : Table = dbConfig.getPasswordTable()
# conn = dbConfig.getConnection()

# user_table.insert().values(account_name = "test", master_password ="master_pwd")
# select_st = user_table.select().where(
#    user_table.c.account_name == 'test')
# res = conn.execute(select_st)
# for _row in res:
#     print(_row)

# print(select(user_table).where(user_table.c.account_name == "test"))