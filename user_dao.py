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
		try:
			insert = self.user_table.insert().values(account_name = user.account_name, master_password = hash_text(user.master_password))
			self.conn.execute(insert)
			return True
		except:
			return False

	def get_user_by_account_name(self, account_name: str):
		result = []
		try:
			select_st = self.user_table.select().where(self.user_table.c.account_name == account_name)
			res = self.conn.execute(select_st)
			for _row in res:
			    result.append(self.__mapper(_row))
			return result
		except:
			return result

	def get_user_by_details(self, user: User):
		result = []
		try:
			select_st = self.user_table.select().where(self.user_table.c.account_name == user.account_name, 
					self.user_table.c.master_password == hash_text(user.master_password))
			res = self.conn.execute(select_st)
			for _row in res:
			    result.append(self.__mapper(_row))
			return result
		except:
			return result

	def delete_user(self, user: User):
		try:
			if len(self.get_user_by_details(user)) != 0:
				del_st = self.user_table.delete().where(
					self.user_table.c.account_name == user.account_name, 
					self.user_table.c.master_password == hash_text(user.master_password))
				res = self.conn.execute(del_st)
				return True
			else:
				return False
		except:
			return False

	def update_user(self, old_user: User, new_user: User):
		try:
			if self.delete_user(old_user):
				self.insert_user(new_user)
				return True
			else:
				return False
		except:
			return False

# runner
# dbConfig = DatabaseConfig()
# dbConfig.create_table()
# UserDao(dbConfig).insert_user(User(account_name = "test", master_password="pwd"))
# print(len(UserDao(dbConfig).get_user_by_account_name("test")))
# UserDao(dbConfig).delete_user(User(account_name = "test", master_password="pwd"))
# print(len(UserDao(dbConfig).get_user_by_account_name("test")))
# UserDao(dbConfig).update_user(User(account_name = "test", master_password="pwd1"),User(account_name = "test", master_password="pwd1"))

