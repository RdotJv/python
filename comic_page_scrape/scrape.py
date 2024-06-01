import bs4, requests, pprint, webbrowser, pathlib, zipfile
from pathlib import Path
url = 'https://xkcd.com'
reset_url = url

for i in range(100):
  response = requests.get(url)
  response.raise_for_status()

  soup = bs4.BeautifulSoup(response.text, 'html.parser')

  image_path = soup.select('div#comic > img')[0].get('src')
  current_comic = 'https:'+ image_path
  comic_name = image_path.split('/')[-1]

  destination = pathlib.Path.cwd()/'comic_page_scrape'/'xkcd'/comic_name

  with open(destination, 'wb') as comic:
    responseimg = requests.get(current_comic)
    responseimg.raise_for_status()

    for chunk in responseimg.iter_content(100000):
      comic.write(chunk)
  url = reset_url + soup.select("a[rel='prev']")[0].get('href')
 
  print('fetching', url)