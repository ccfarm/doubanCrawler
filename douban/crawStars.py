from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

f = open('MovieList.txt', 'r')
allLines = f.read()
lines = allLines.split('\n')
f.close()

process = CrawlerProcess(get_project_settings())

for i in range(500):
    line = lines[i]
    if (line != ''):
        url = 'https://movie.douban.com/subject/' + line + '/celebrities'
        #f = craw(url=url)
        #print(url + '\n')
        process.crawl('movie', url=url)
    #i = i+ 1


process.start()

