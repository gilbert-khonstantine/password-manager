from db_config import DatabaseConfig
from encrypt_hash import encrypt_text, decrypt_text
import os 
from dotenv import load_dotenv

load_dotenv()

class Password:
	def __init__(self, account: str, platform :str, username: str, email: str, password: str):
		self.account = account
		self.platform = platform
		self.email = email
		self.username = username
		self.password = password

	def __repr__(self):
		return f'platform = {self.platform}, username = {self.username}, password = {self.password}'


class PasswordDao:
	def __init__(self, dbConfig: DatabaseConfig):
		self.dbConfig : DatabaseConfig = dbConfig
		self.password_table : Table = self.dbConfig.getPasswordTable()
		self.conn = dbConfig.getConnection()

	def __mapper(self, db_result):
		return Password(db_result[1], db_result[2], db_result[3], db_result[4], decrypt_text(db_result[5]))

	def insert_password(self, password: Password):
		try:
			insert = self.password_table.insert().values(account = password.account, platform = password.platform, username = password.username, email = password.email , password = encrypt_text(password.password))
			self.conn.execute(insert)
			return True
		except:
			return False

	def get_pwd_by_platform(self, account: str, platform: str):
		result = []
		try:
			select_st = self.password_table.select().where(self.password_table.c.platform == platform, self.password_table.c.account == account)
			res = self.conn.execute(select_st)
			for _row in res:
			    result.append(self.__mapper(_row))
			return result
		except:
			return result

	def get_pwd_by_account(self, account: str):
		result = []
		try:
			select_st = self.password_table.select().where(self.password_table.c.account == account)
			res = self.conn.execute(select_st)
			for _row in res:
			    result.append(self.__mapper(_row))
			return result
		except:
			return result

	def delete_password(self, password: Password):
		try:
			if self.get_pwd_by_platform(password.account, password.platform)[0].password == password.password:
				del_st = self.password_table.delete().where(
						self.password_table.c.username == password.username,
						self.password_table.c.email == password.email,
						self.password_table.c.account == password.account,
						self.password_table.c.platform == password.platform)
				res = self.conn.execute(del_st)
				return True
			else: 
				return False
		except:
			return False

	def update_password(self, old_password: Password, new_password: Password):
		try:
			if self.delete_password(old_password):
				self.insert_password(new_password)
				return True
			else:
				return False
		except:
			return False


# runner code
# dbConfig : DatabaseConfig = DatabaseConfig()
# dbConfig.create_table()
# dbConfig.password
# PasswordDao(dbConfig).insert_password(Password(account = "test2", platform = "fb", username = "beta_user", email = "beta@gmail.com", password = "secret"))
# print(PasswordDao(dbConfig).get_pwd_by_platform("test2", "fb"))
# PasswordDao(dbConfig).delete_password(Password(account = "test2", platform = "fb", username = "beta_user", email = "beta@gmail.com", password = "secret"))
# print(PasswordDao(dbConfig).get_pwd_by_platform("test2", "fb"))
# print(PasswordDao(dbConfig).get_pwd_by_account("test3"))