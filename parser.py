import requests
from bs4 import BeautifulSoup


def normalize(tag):
    string = str(tag)
    if string =="<br/>":
        return "\r\n"
    if "Припев" in string:
        return ""
    if "strong" in string:
        string = string.replace('<strong>', "").replace("</strong>", "")
    if "Куплет" in string or "куплет" in string:
        return ""
    for i in range(10):
        string = string.replace(str(i), "")
    if '|' in string:
        string = string[:string.index('|')]
    if 'x' in string:
        string = string[:string.index('x')]
    if 'p' in string:
        string = string.replace("<p>", "").replace('</p>', "")
    if 'br' in string:
        string = string.replace('<br/>', '').replace('<br>', '')
    return string.replace('(', "").replace(')',"")

baseurl = 'https://www.beesona.ru/'
songlinks = []
numpages = 6
for i in range(numpages):
    request = requests.get('https://www.beesona.ru/songs/korol_i_shut/p'+str(i+1))
    soup = BeautifulSoup(request.text, features="lxml")
    table = soup.find_all('table')[0]
    for link in table.find_all('a', href=True):
        songlinks.append(baseurl+link['href'])

with open('data.txt', 'w') as datafile:
    for link in songlinks:
        request = requests.get(link)
        soup = BeautifulSoup(request.text, features="lxml")
        div = soup.find_all('div', attrs={'class': 'm207'})
        contents = div[0].contents
        #text = div[0].next_sibling
        string = "".join(list(map(normalize, contents))[:-1])
        #print(text)
        print(string)
        datafile.write(string)

