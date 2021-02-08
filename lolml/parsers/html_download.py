import requests
from urllib.request import urlopen
# establishing session
s = requests.Session()
s.headers.update({
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'

})


def load_user_data(page, session):
    url = 'https://www.cybersport.ru/base/tournaments?sort=title&filterOrder=auto&disciplines=23955&status=past&page=%d' % (page)
    request = session.get(url)
    page = urlopen(url)
    print(page.info().get_content_charset())
    return request.text


def contain_movies_data(text):
    soup = BeautifulSoup(text)
    film_list = soup.find('div', {'class': 'profileFilmsList'})
    return film_list is not None


# loading files
page = 1
"""
while True:
    data = load_user_data(user_id, page, s)
    if contain_movies_data(data):
        with open('./page_%d.html' % (page), 'w') as output_file:
            output_file.write(data.encode('cp1251'))
            page += 1
    else:
        break
"""


#print(page.info().get_content_charset())
while page <= 3:
    data = load_user_data(page, s)
    with open('./page_%d.html' % (page), 'w') as output_file:
            output_file.write(str(data.encode('utf-8')))
            page += 1
