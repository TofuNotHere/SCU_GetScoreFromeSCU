#author: Chenshufu
#date:2015年12月15日15:32:02
from urllib import request, parse
from http import cookiejar
from bs4 import BeautifulSoup

def myAlign(string, length = 0):
    if length == 0:
        return string
    placeholder = u'　'
    slen = len(string)
    while slen < length:
        string += placeholder
        slen += 1
    return string

def getScoreText(x):
    return x.text.strip()

def getScore(htmldoc):
    soup = BeautifulSoup(htmldoc.read().decode('gbk'),'html.parser')
    tmp = soup.find_all('tr',onmouseout="this.className='even';")
    scoreList = []
    for x in tmp:
        scoreList.append(list(map(getScoreText,[x.contents[5],x.contents[11],x.contents[13]])))
    return scoreList

def showScore(scoreList):
    for ele in scoreList:
        print(myAlign(ele[0],20)+myAlign(ele[1],10)+myAlign(ele[2]))

def initLoginData():
    username = input('学号:')
    passwd = input('密码:')
    print("Login...")
    login_data = parse.urlencode([
        ('zjh', username),
        ('mm', passwd),
    ])
    return login_data

#cookie操作 & 报表头
def initOpener():
    cookie = cookiejar.CookieJar()
    opener=request.build_opener(request.HTTPCookieProcessor(cookie))
    opener.addheaders = [
       ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    ,('Cache-Control','max-age=0')
    ,('Host','202.115.47.141')
    ,('Connection','keep-alive')
    ,('Origin', 'http://202.115.47.141')
    ,('DNT','1')
    ,('Content-Length','197')
    ,('Upgrade-Insecure-Requests','1')
    ,('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]
    return opener



Score_url = 'http://202.115.47.141/bxqcjcxAction.do'
Score_data = parse.urlencode([('totalrows','300'),
    ('pageSize', '300')])
login_url = 'http://202.115.47.141/loginAction.do'

try:
    opener = initOpener()
    login_data = initLoginData()
    ht = opener.open(login_url,login_data.encode('gbk')) #登陆并获取cookie
    #print(ht.read().decode('gbk'))#debug测试
    htmldoc = opener.open(Score_url,Score_data.encode('gbk'))  #获取列表
    #print(htmldoc.read().decode('gbk'))
    showScore(getScore(htmldoc))
    #print(tmp)
except:
    print('失败了 ╮(╯▽╰)╭')
input('Press <enter> to exit!')
