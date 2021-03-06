# coding=utf-8
import json
import os
from Movie import Movie
import pymysql
import requests
from functions import log, change_ip
from api import api, tags


# 获取电影信息
def get_information():
    for tag in tags:
        movies = []
        start = 0
        while True:
            try:
                params = {
                    'tags': '电影,' + tag,
                    'start': start
                }
                content = requests.get(url=api[0], params=params)
                data = json.loads(str(content.content, 'utf-8'))['data']
                if len(data) != 0:
                    movies.extend(data)
                    print(tag, len(movies))
                    start += len(data)
                else:
                    log(
                        '——————————————————————————————————————————————————————————————————————————————————\n' + tag + 'is over.And There are %s movies' % len(
                            movies))
                    with open('movies/%s.json' % tag, 'w') as file:
                        json.dump(movies, file)
                    exit()
            except Exception as message:
                with open('movies/%s.json' % tag, 'w') as file:
                    json.dump(movies, file)
                    log(str(message) + '\n' + tag + str(start), 1)


def get_movies(cursor):
    for root, dir, files in os.walk('movies'):
        for filename in files:
            if str(filename).endswith('.finished'):
                continue
            number = 0
            with open('movies/%s' % filename, 'r') as file:
                movies = json.load(file)
            try:
                for i in movies:
                    cursor.execute("select exists (select * from movies where id=%s)" % i['id'])  # 判断是否重复
                    if cursor.fetchone()[0] == 1:
                        number += 1
                        continue
                    movie = Movie(i)
                    sql = "INSERT INTO movies(TITLE,ID,DIRECTORS,SCREENWRITER,KINDS,AREA,CASTS,RATE,STAR,IMAGE,PLOT,RELEASE_DATE,RUNTIME) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
                        "\"" + movie.title + "\"", movie.id, "\"" + movie.dircetors + "\"",
                        "\"" + movie.screenwriter + "\"", "\"" + movie.type + "\"", "\"" + filename[:-5] + "\"",
                        "\"" + movie.casts + "\"", movie.rate, movie.star,
                        "\"" + movie.image + "\"", "\"" + movie.plot.replace("\"", "'") + "\"",
                        "\"" + movie.date + "\"", "\"" + movie.runtime + "\"")
                    cursor.execute(sql)
                    number += 1
                    if number % 100 == 0:
                        db.commit()
                    log(filename[:-5] + '第' + str(number) + '部电影--' + movie.title + '--id:' + movie.id + '收录完成')
                db.commit()
            except Exception as message:
                db.commit()
                print(sql)
                log(filename[:-5] + str(message), 1)
                exit()

            os.rename('movies/%s' % filename, 'movies/%s' % filename + '.finished')


if __name__ == '__main__':
    # get_information()
    db = pymysql.connect("localhost", 'root', 'root', 'film_recommendation', charset='utf8')
    cursor = db.cursor()
    try:
        get_movies(cursor)
    except:
        log("主动停止")
        exit()
        db.commit()
