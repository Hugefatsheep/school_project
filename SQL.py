import pymysql

db = pymysql.connect("localhost", 'root', 'root', 'film_recommendation',charset='utf8')
cursor = db.cursor()
sql = [
    """
    create table movies(
                    TITLE CHAR (255),
                    ID INT ,
                    DIRECTORS TEXT,
                    SCREENWRITER TEXT,
                    KINDS TEXT,
                    AREA TEXT,
                    CASTS TEXT,
                    RATE FLOAT ,
                    STAR FLOAT ,
                    IMAGE CHAR (255),
                    RELEASE_DATE CHAR (255),
                    PLOT TEXT ,
                    RUNTIME CHAR (255))
                    
    """,
    """ 
                    CREATE TABLE comments_users(NAME CHAR (30),ID INT ,COMMENTS TEXT)""",

]
#for i in sql:
#    cursor.execute(i)
#    db.commit()
cursor.execute(sql[0])
db.commit()
db.close()
