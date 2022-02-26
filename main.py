from db_config import DatabaseConfig
from password_dao import PasswordDao, Password
from user_dao import UserDao, User
from authentication import authenticated, is_new_user

db_config : DatabaseConfig = DatabaseConfig()
db_config.create_table()
user_dao : UserDao = UserDao(db_config)
password_dao : PasswordDao = PasswordDao(db_config)

def print_details(details: list):
	print("==================================================")
	if len(details) == 0:
		print("No records found in our system")
	else: 
		for detail in details:
			print(detail)
	print("==================================================")

def get_password_details(account_name : str):
	app_name = str(input("app name: "))
	username = str(input("username: "))
	email = str(input("email: "))
	pwd = str(input("password: "))
	return Password(account_name, app_name, username, email, pwd)

def get_user_details(account_name : str):
	master_key = str(input("master key: "))
	return User(account_name, master_key)

if __name__ == '__main__':
	account_name = str(input("telegram username: "))
	while True:
		if is_new_user(account_name, user_dao):
			new_master_key = str(input("Welcome! You are our new user\nCreate your master key: "))
			user_dao.insert_user(User(account_name, new_master_key))
		else:
			print("You are registered in our system! Do you want to:")
			print("1. Retrieve password for an app")
			print("2. View All passwords")
			print("3. Store new password")
			print("4. Update password")
			print("5. Delete password")
			print("6. Update master key")
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
						print("Please insert your password details: ")
						password : Password = get_password_details(account_name)
						if password_dao.insert_password(password):
							print("Password stored successfully")
						else:
							print("The details might be incorrect, please try again")
					elif user_intention == '4':
						print("Please insert your OLD password details: ")
						old_password : Password = get_password_details(account_name)
						print("Please insert your NEW password details: ")
						new_pwd = input("Your new password: ")
						new_password : Password = Password(old_password.account, old_password.platform, old_password.username, old_password.email, new_pwd)
						if password_dao.update_password(old_password, new_password):
							print("Password updated successfully")
						else:
							print("The details might be incorrect, please try again")
					elif user_intention == '5':
						print("Please insert the details of the password to be deleted: ")
						password : Password = get_password_details(account_name)
						if password_dao.delete_password(password):
							print("Password removed successfully")
						else:
							print("The details might be incorrect, please try again")
					elif user_intention == '6':
						print("Please insert your OLD account details: ")
						old_user : User = get_user_details(account_name)
						print("Please insert your NEW account details: ")
						new_user : User = get_user_details(account_name)
						if user_dao.update_user(old_user, new_user):
							print("Account updated successfully")
						else:
							print("The details might be incorrect, please try again")
					else:
						print("Sorry, I dont understand your choice, please retry.")
				else:
					print("incorrect password")
			else: 
				break