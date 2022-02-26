from db_config import DatabaseConfig
from password_dao import PasswordDao, Password
from user_dao import UserDao, User
from authentication import authenticated, new_user

db_config : DatabaseConfig = DatabaseConfig()
db_config.create_table()
user_dao : UserDao = UserDao(db_config)
password_dao : PasswordDao = PasswordDao(db_config)

def print_details(details: list):
	print("=======================================")
	if len(details) == 0:
		print("No records found in our system")
	else: 
		for detail in details:
			print(detail)
	print("=======================================")

if __name__ == '__main__':
	account_name = str(input("telegram username: "))
	while True:
		if new_user(account_name, user_dao):
			new_master_key = str(input("Welcome! You are our new user\nCreate your master key: "))
			user_dao.insert_user(User(account_name, new_master_key))
		else:
			print("You are registered in our system! Do you want to:")
			print("1. Retrieve password for an app")
			print("2. View All passwords")
			print("3. Store new password")
			print("To Exit, press Q:")
			user_intention = str(input("your input: "))
			if user_intention.lower() != 'q':
				entered_password = input("Please enter your password: ")
				if authenticated(account_name, entered_password, user_dao):
					if user_intention == '1':
						platform_name = input("what app are you searching for?\n")
						details = password_dao.get_pwd_by_platform(account_name, platform_name)
						print_details(details)
					elif user_intention == '2':
						details = password_dao.get_pwd_by_account(account_name)
						print_details(details)
					elif user_intention == '3':
						app_name = str(input("app name: "))
						username = str(input("username: "))
						email = str(input("email: "))
						pwd = str(input("password: "))
						password_dao.insert_password(Password(account_name, app_name, username, email, pwd))
					else:
						print("Sorry, I dont understand your choice, please retry.")
				else:
					print("incorrect password")
			else: 
				break