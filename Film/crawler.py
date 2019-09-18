# _*_ coding: utf-8 _*_
# @time     : 2018/5/11 10:34
# @Author   : liying
# @FileName : crawler.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import urllib, re, time, os, random

class Crawler(object):

    def __init__(self, url):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",}
        self.url = url
        req = urllib.request.Request(self.url, headers=self.headers)
        response = urllib.request.urlopen(req)
        self.html = response.read()
        self.soup = BeautifulSoup(self.html, 'lxml')

    #电影海报
    def get_posters(self):
        imageSavePath = r'E:/far sight/PyCharmProjects/Film/static_files/img/poster'
        os.chdir(os.path.join(os.getcwd(), imageSavePath))
        for i in self.soup.find_all('div', attrs={"class": "pic"}):
            pic_name = str(i.find('img').get('alt')) + '.jpg'
            img_src = i.find('img').get('src')
            urllib.request.urlretrieve(img_src, pic_name)

    #简介
    def get_intros(self):
        self.intros = []
        self.result_intros = self.soup.find_all('span', attrs={'class': 'inq'})

        for i in range(25):
            try:
                self.intros.append(self.result_intros[i].string)
            except:
                self.intros.append(' ')
        return self.intros

    #信息详情页url
    def get_info_page_urls(self):
        self.info_page_urls = []
        self.result_html = self.soup.find(attrs={'class': 'grid_view'})
        self.result_box = self.result_html.find_all('div',attrs={'class':'hd'})
        for i in self.result_box:
            self.result_info_page_urls = i.find_all('a')
            for j in self.result_info_page_urls:
                self.info_page_urls.append(j['href'])
        return self.info_page_urls

    #电影名
    def get_names(self):
        self.names = []
        self.result_html = self.soup.find(attrs={'class': 'grid_view'})
        self.result_box = self.result_html.find_all('div',attrs={'class':'hd'})
        for i in self.result_box:
            self.result_name = i.find_all('span', attrs={'class': 'title'})
            temp_name = self.result_name[0].string
            self.names.append(temp_name)
        return self.names

    #详情页
    def info_page(self):
        self.directors = []
        self.writers = []
        self.actors = []
        self.types = []
        self.YouKu_urls = []
        self.TengXun_urls = []
        self.SouHu_urls = []
        self.AiQiYi_urls = []
        self.contents = []
        self.show_times = []
        self.run_times = []
        self.grades = []
        self.countrys = []
        self.languages = []
        for i in self.info_page_urls:
            time.sleep(random.uniform(3, 6))
            try:
                response = urllib.request.urlopen(i)
                self.html2 = response.read()
                self.soup2 = BeautifulSoup(self.html2, 'lxml')
                self.result_html2 = self.soup2.find('div', attrs={'id': 'info'})

                #导演
                self.return_directors = self.result_html2.find_all('a', {'rel': 'v:directedBy'})
                self.directors.append(self.return_directors[0].string)
                # print(self.directors)

                #编剧
                self.return_writers = self.soup2.select('#info span[class="attrs"]')[1].find_all('a')
                temp = []
                for i in self.return_writers:
                    temp.append(i.string)
                self.writers.append(' / '.join(temp))
                # print(self.writers)

                #主演
                self.return_actors = self.result_html2.find_all('a', attrs={'rel':'v:starring'})
                temp = []
                for i in self.return_actors:
                    temp.append(i.string)
                self.actors.append(' / '.join(temp))
                # print(self.actors)

                #类型
                self.return_types = self.result_html2.find_all('span', attrs={'property': 'v:genre'})
                temp = []
                for i in self.return_types:
                    temp.append(i.string)
                self.types.append(' / '.join(temp))
                # print(self.types)

                #视频链接(优酷/腾讯/搜狐/爱奇艺)
                self.result_plays = self.soup2.find('div', attrs={'class': 'gray_ad'})
                self.return_YouKu_urls = self.result_plays.find_all('a', attrs={'data-cn': '优酷视频'})
                self.return_Tengxun_urls = self.result_plays.find_all('a', attrs={'data-cn': '腾讯视频'})
                self.return_SouHu_urls = self.result_plays.find_all('a', attrs={'data-cn': '搜狐视频'})
                self.return_AiQiYi_urls = self.result_plays.find_all('a', attrs={'data-cn': '爱奇艺视频'})

                if self.return_YouKu_urls:
                    for i in self.return_YouKu_urls:
                        self.YouKu_urls.append(i['href'])
                else:
                    self.YouKu_urls.append(' ')

                if self.return_Tengxun_urls:
                    for i in self.return_Tengxun_urls:
                        self.TengXun_urls.append(i['href'])
                else:
                    self.TengXun_urls.append(' ')

                if self.return_SouHu_urls:
                    for i in self.return_SouHu_urls:
                        self.SouHu_urls.append(i['href'])
                else:
                    self.SouHu_urls.append(' ')

                if self.return_AiQiYi_urls:
                    for i in self.return_AiQiYi_urls:
                        self.AiQiYi_urls.append(i['href'])
                else:
                    self.AiQiYi_urls.append(' ')

                #剧情介绍
                self.return_contents = self.soup2.find_all('span', attrs={'property': 'v:summary'})
                pattern = re.compile(r'<span.*?property="v:summary">.*?\u3000\u3000(.*?)\n.*?</span>', re.S)
                if self.return_contents:
                    temp = re.search(pattern, str(self.return_contents)).group(1)
                    self.contents.append(temp)
                else:
                    self.contents.append(' ')
                # print(self.contents)

                #上映时间
                self.return_show_times = self.soup2.find_all('span', attrs={'property': 'v:initialReleaseDate'})
                temp = []
                for i in self.return_show_times:
                    temp.append(i.string)
                self.show_times.append(' / '.join(temp))
                # print(self.show_times)

                #片长
                self.return_run_times = self.soup2.find_all('span', attrs={'property': 'v:runtime'})
                temp = []
                for i in self.return_run_times:
                    temp.append(i.string)
                self.run_times.append(' / '.join(temp))
                # print(self.run_times)

                #评分
                self.return_grades = self.soup2.find_all('strong', attrs={'property': 'v:average'})
                self.grades.append(self.return_grades[0].string)
                # print(self.grades)

                #国家/地区和语言
                pattern = re.compile(r'<span.*?class="pl">制片国家/地区:</span> (.+?)<br/>.*?<span.*?class="pl">语言:</span> (.+?)<br/>', re.S)
                self.countrys.append(re.search(pattern, str(self.soup2)).group(1))
                self.languages.append(re.search(pattern, str(self.soup2)).group(2))
                # print(self.countrys)
                # print(self.languages)

            except:
                self.directors.append(' ')
                self.writers.append(' ')
                self.actors.append(' ')
                self.types.append(' ')
                self.YouKu_urls.append(' ')
                self.TengXun_urls.append(' ')
                self.SouHu_urls.append(' ')
                self.AiQiYi_urls.append(' ')
                self.contents.append(' ')
                self.show_times.append(' ')
                self.run_times.append(' ')
                self.grades.append(' ')
                self.countrys.append(' ')
                self.languages.append(' ')

        return self.directors, self.writers, self.actors, self.types, self.YouKu_urls, self.TengXun_urls, \
               self.SouHu_urls, self.AiQiYi_urls, self.contents, self.show_times, self.run_times, self.grades, \
               self.countrys, self.languages

    def test(self):
        self.writers = []
        for i in self.info_page_urls:
            time.sleep(random.uniform(3, 5))
            # print(1)
            # try:
            response = urllib.request.urlopen(i)
            self.html2 = response.read()
            self.soup2 = BeautifulSoup(self.html2, 'lxml')
            self.return_writers = self.soup2.select('#info span[class="attrs"]')[1].find_all('a')
            temp = []
            for i in self.return_writers:
                temp.append(i.string)
            self.writers.append(' / '.join(temp))
            # print(self.writers)
            # except:
            #     self.writers.append(' ')

if __name__ == '__main__':
    names = []
    intros = []
    info_page_urls = []
    directors = []
    writers = []
    actors = []
    types = []
    YouKu_urls = []
    TengXun_urls = []
    SouHu_urls = []
    AiQiYi_urls = []
    contents = []
    show_times = []
    run_times = []
    grades = []
    countrys = []
    languages = []
    for i in range(10):
        print('-'*40)
        print('第%d页爬取开始...'%(i+1))
        print('-'*40)

        variate = i*25
        crawler = Crawler('https://movie.douban.com/top250?start='+str(variate)+'&filter=')

        names += crawler.get_names()
        intros += crawler.get_intros()
        info_page_urls += crawler.get_info_page_urls()
        # 电影海报下载
        crawler.get_posters()

        directors, writers, actors, types, YouKu_urls, TengXun_urls, SouHu_urls, AiQiYi_urls, contents, show_times, \
        run_times, grades, countrys, languages = crawler.info_page()

        directors += directors
        writers += writers
        actors += actors
        types += types
        YouKu_urls += YouKu_urls
        TengXun_urls += TengXun_urls
        SouHu_urls += SouHu_urls
        AiQiYi_urls += AiQiYi_urls
        contents += contents
        show_times += show_times
        run_times += run_times
        grades += grades
        countrys += countrys
        languages += languages

        print('电影名: ',names)
        print('简介: ',intros)
        print('详情页url: ',info_page_urls)
        print('导演: ',directors)
        print('编剧: ',writers)
        print('主演: ',actors)
        print('类型: ',types)
        print('优酷视频链接: ',YouKu_urls)
        print('腾讯视频链接: ',TengXun_urls)
        print('搜狐视频链接: ',SouHu_urls)
        print('爱奇艺视频链接: ',AiQiYi_urls)
        print('电影详情: ',contents)
        print('上映时间: ',show_times)
        print('片长: ',run_times)
        print('评分: ',grades)
        print('国家/地区: ',countrys)
        print('语言: ',languages)
        print('-'*40)
        print('第%d页已爬取完成'%(i+1))
        print('-'*40)

        # print(crawler.test())
