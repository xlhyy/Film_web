# _*_ coding: utf-8 _*_
# @time     : 2018/5/11 10:58
# @Author   : liying
# @FileName : add_crawlerdata_to_db.py
# @Software : PyCharm

import random
import crawler
import MySQLHelper

def main():
    myhelper_obj = MySQLHelper.MySQLHelper('127.0.0.1',3306,'film','root','root','utf8')
    myhelper_obj.getConn()
    for i in range(10):

        print('-' * 40)
        print('第%d页爬取开始...' % (i + 1))
        print('-' * 40)

        variate = i*25
        crawlerobj = crawler.Crawler('https://movie.douban.com/top250?start='+str(variate)+'&filter=')
        names = crawlerobj.get_names()
        intros = crawlerobj.get_intros()
        crawlerobj.get_info_page_urls()
        crawlerobj.get_posters()

        directors, writers, actors, types, YouKu_urls, TengXun_urls, SouHu_urls, AiQiYi_urls, contents, show_times, \
        run_times, grades, countrys, languages = crawlerobj.info_page()
        posters = []
        for j in range(len(names)):
            posters.append('img/poster/' + names[j] + '.jpg')
            sql = 'INSERT INTO film_app_filminfo(names, posters, grades, directors, writers, actors, types, countrys, \
                  languages, show_times, run_times, intros, contents, YouKu_urls, TengXun_urls, SouHu_urls, AiQiYi_urls\
                  ) VALUES(%s, %s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)'
            params = [names[j],posters[j], grades[j], directors[j], writers[j], actors[j], types[j], countrys[j], \
                      languages[j], show_times[j], run_times[j], intros[j], contents[j], YouKu_urls[j], TengXun_urls[j], \
                      SouHu_urls[j], AiQiYi_urls[j]]

            print(params)
            myhelper_obj.insert(sql,params=params)

        print('-' * 40)
        print('第%d页爬取完成' % (i + 1))
        print('-' * 40)

    myhelper_obj.closeConn()

if __name__ == '__main__':
    main()