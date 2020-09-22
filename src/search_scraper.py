# from googlesearch import search
# #pip3 install google
#
# for url in search('IDEX', tld='com', stop=1):
#     print(url)

from GoogleNews import GoogleNews
#pip3 install GoogleNews

googlenews = GoogleNews()

googlenews = GoogleNews(lang='en')

googlenews = GoogleNews(period='d')

googlenews = GoogleNews(start='06/12/2020',end='09/20/2020')

googlenews = GoogleNews(encode='utf-8')

googlenews.search('IDEX')

googlenews.getpage(2)

print(googlenews.result())

googlenews.gettext()
