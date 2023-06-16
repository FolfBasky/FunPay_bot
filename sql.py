import sqlite3

# Define a function to create user profiles table
def create_user_profiles_table():
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                active INTEGER DEFAULT 1,
                login TEXT NOT NULL UNIQUE,\n                password TEXT NOT NULL,
                number_phone TEXT NOT NULL,
                number_card TEXT DEFAULT NULL
            );
        """
        cursor.execute(create_table)

# Define a function to add a new user profile
def add_user_profile(active, login, password, number_phone, number_card=None):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        add_profile = """
            INSERT INTO user_profiles (active, login, password, number_phone, number_card)
            VALUES (?, ?, ?, ?, ?)
        """
        profile_data = (active, login, password, number_phone, number_card)
        cursor.execute(add_profile, profile_data)
    return True

# Define a function to get the details of the first active account
def get_first_active_account_info():
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            SELECT login, password, number_phone, number_card FROM user_profiles WHERE active = 1
        """
        cursor.execute(query)
        result = cursor.fetchone()

    if result:
        result = {
            'login':result[0],
            'password':result[1],
            'phone_number':result[2],
            'card_number':result[3],
        }

    return result


def set_active_status_accounts(active=False):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            UPDATE user_profiles SET active = ?
        """
        cursor.execute(query, (int(active),))

# Define a function to set the active status of a user profile
def set_account_active(login, active:int):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            UPDATE user_profiles SET active = ? WHERE login = ?
        """
        cursor.execute(query, (int(active), login,))

# Define a function to add a card number to a user profile
def add_card_number(login, card_number):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            UPDATE user_profiles SET number_card = ? WHERE login = ?
        """
        cursor.execute(query, (card_number, login,))

# Define a function to delete a user profile
def delete_user(login):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            DELETE FROM user_profiles WHERE login = ?
        """
        cursor.execute(query, (login,))
    return True

# Define a function to get the details of all user profiles
def get_all_profiles():
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            SELECT active, login, password, number_phone, number_card FROM user_profiles
        """
        cursor.execute(query)
        ver = cursor.fetchall()
    
    result = []
    for v in ver:
        data = {
            'active':v[0],
            'login':v[1],
            'password':v[2],
            'phone_number':v[3],
            'card_number':v[4],
        }
        result.append(data)

    return result

def create_vk_base():
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS vk_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                active INTEGER DEFAULT 1,
                login TEXT NOT NULL UNIQUE,
                access_token TEXT NOT NULL,
                user_id INTEGER DEFAULT NULL
            );
        """
        cursor.execute(create_table)

def add_vk_account(login, access_token, user_id):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO vk_profiles (login, access_token, user_id) VALUES (?, ?, ?);
        """
        cursor.execute(insert_query, (login, access_token, user_id))

def choice_active_status_vk_account(login, active=True):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            UPDATE vk_profiles SET active = ? WHERE login = ?
        """
        cursor.execute(query, (int(active), login,))

def set_active_status_vk_accounts(active=False):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            UPDATE vk_profiles SET active = ?
        """
        cursor.execute(query, (int(active),))

def select_all_vk_profiles():
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        select_query = """
            SELECT * FROM vk_profiles;
        """
        cursor.execute(select_query)
        data = []
        for id,active,login,access_token,user_id in cursor.fetchall():
            result = {}
            result['id'] = id
            result['active'] = active
            result['login'] = login
            result['access_token'] = access_token
            result['user_id'] = user_id
            data.append(result)
        return data

def delete_vk_account(login):
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        delete_query = """
            DELETE FROM vk_profiles WHERE login = ?;
        """
        cursor.execute(delete_query, (login,))

def get_first_active_account_vk_info():
    with sqlite3.connect('user_profiles.db') as conn:
        cursor = conn.cursor()
        query = """
            SELECT login, access_token, user_id FROM vk_profiles WHERE active = 1
        """
        cursor.execute(query)
        result = cursor.fetchone()

    if result:
        result = {
            'login':result[0],
            'access_token':result[1],
            'user_id':result[2],
        }
    return result


# Create the user profiles table
create_user_profiles_table()
create_vk_base()
if __name__ == "__main__":
   pass
   """ # Test the functions
    add_user_profile(1,'user1','12345','2345')
    add_user_profile(0,'user2','12345','2345','7845')
    add_user_profile(1,'user3','12345','2345','7562')

    add_card_number('user1','1234')
    print(get_first_active_account_info())
    set_account_active('user1',0)
    print(get_first_active_account_info())

    print(get_all_profiles())"""