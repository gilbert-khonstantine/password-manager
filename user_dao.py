from db_config import DatabaseConfig
from encrypt_hash import hash_text
from dotenv import load_dotenv

load_dotenv()
class User:
	def __init__(self, account_name: str, master_password: str):
		self.account_name = account_name
		self.master_password = master_password

	def __repr__(self):
		return f'User(account_name = {self.account_name}, pwd = ${self.master_password})'

class UserDao:
	def __init__(self, dbConfig: DatabaseConfig):
		self.dbConfig : DatabaseConfig = dbConfig
		self.user_table : Table = self.dbConfig.getUserTable()
		self.conn = dbConfig.getConnection()

	def __mapper(self, db_result):
		return User(db_result[1], db_result[2])

	def insert_user(self, user: User):
		insert = self.user_table.insert().values(account_name = user.account_name, master_password = hash_text(user.master_password))
		self.conn.execute(insert)
		return

	def get_user_by_account_name(self, account_name: str):
		result = []
		select_st = self.user_table.select().where(self.user_table.c.account_name == account_name)
		res = self.conn.execute(select_st)
		for _row in res:
		    result.append(self.__mapper(_row))
		return result

	def update_user(self, user: User):
		# TODO
		pass

	def delete_user(self, user: User):
		# TODO
		pass

# runner
# dbConfig = DatabaseConfig()
# dbConfig.create_table()
# UserDao(dbConfig).insert_user(User(account_name = "test2", master_password="pwd"))
# print(UserDao(dbConfig).get_user_by_account_name("test"))
# print(UserDao(dbConfig).get_user_by_account_name("test2"))