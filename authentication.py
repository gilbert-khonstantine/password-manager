from user_dao import UserDao
from password_dao import PasswordDao
from encrypt_hash import hash_text

def is_new_user(username: str, user_dao: UserDao) -> bool:
	return len(user_dao.get_user_by_account_name(username)) == 0

def authenticated(username: str, password: str, user_dao: UserDao) -> bool:
	user = user_dao.get_user_by_account_name(username)[0]
	return user.master_password == hash_text(password)