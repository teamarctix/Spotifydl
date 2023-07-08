import psycopg2


conn = psycopg2.connect(database="emlvwsts",
                        host="mahmud.db.elephantsql.com",
                        user="emlvwsts",
                        password="QZplqRjrPc5y3n2cf6VwgdvhcUZJ1hXV",
                        port="5432")

cursor = conn.cursor()

def create_table():
  
  sql ='''CREATE TABLE Music(
   NAME VARCHAR(255) NOT NULL
   URL VARCHAR(255) NOT NULL
)'''

  cursor.execute(sql)
  print("Table created successfully........")
  conn.commit()


def insert_db(name,url):
    query = "INSERT INTO Music (name,url) VALUES('{}','{}')".format(name,url)
    cursor.execute(query)
    conn.commit()

def read_db():
   cursor.execute("SELECT * FROM Music")
   data = cursor.fetchall()
   return data

def delall_db(name="Music"):
    cursor.execute(f"DELETE FROM {name}")
    conn.commit()

#cursor.execute("DROP TABLE IF EXISTS PHLinks")
