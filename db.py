import psycopg2


conn = psycopg2.connect(database="emlvwsts",
                        host="mahmud.db.elephantsql.com",
                        user="emlvwsts",
                        password="QZplqRjrPc5y3n2cf6VwgdvhcUZJ1hXV",
                        port="5432")

cursor = conn.cursor()

def create_table():
  
  sql ='''CREATE TABLE Index(
   ID VARCHAR(255) NOT NULL
   URL VARCHAR(255) NOT NULL
)'''

  cursor.execute(sql)
  print("Table created successfully........")
  conn.commit()


def insert_db(lnk):
    query = "INSERT INTO REDLinks (url) VALUES('{}')".format(lnk)
    cursor.execute(query)
    conn.commit()

def read_db():
   cursor.execute("SELECT * FROM REDLinks")
   data = cursor.fetchall()
   return data

def delall_db(name):
    cursor.execute(f"DELETE FROM {name}")
    conn.commit()

#cursor.execute("DROP TABLE IF EXISTS PHLinks")
