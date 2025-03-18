import sqlite3

def save_xpath_and_dom(xpath_name, last_successful_xpath, last_dom):
    conn = sqlite3.connect('locator_database.db')
    cur = conn.cursor()
    query = f'''INSERT INTO locator_db  VALUES ('{xpath_name}', '{last_successful_xpath}','{last_dom}')'''
    cur.execute(query)
    conn.commit()
    conn.close()

def check_if_xpath_exists(xpath_name):
    conn = sqlite3.connect('locator_database.db')
    cur = conn.cursor()
    query = f'''SELECT COUNT(1) FROM locator_db WHERE xpath_name = '{xpath_name}';'''
    cur.execute(query)
    result = (bool([cur.fetchone()][0][0]))
    conn.close()
    return result

def fetch_xpath_entry(xpath_name):
    conn = sqlite3.connect('locator_database.db')
    cur = conn.cursor()
    query = f'''SELECT * FROM locator_db WHERE xpath_name = "{xpath_name}";'''
    cur.execute(query)
    result = cur.fetchone()
    conn.close()
    return result

def update_xpath_entry(xpath_name, last_successful_xpath, last_dom):
    conn = sqlite3.connect('locator_database.db')
    cur = conn.cursor()
    query = f'''UPDATE locator_db SET last_xpath = '{last_successful_xpath}', last_dom = '{last_dom}' WHERE  xpath_name = "{xpath_name}"'''
    cur.execute(query)
    conn.commit()
    conn.close()


# print(fetch_xpath_entry('XPATH_EMPLOYEE_NAME')[1])