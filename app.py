from flask import Flask, render_template

import requests
from bs4 import BeautifulSoup, re


app = Flask(__name__)

BASE_URL = "https://moveek.com/en/" 

def get_URL(URL):
    """Get HTML from(URL)
    """
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def crawl_moveek(URL):
    soup = get_URL(URL)
    movies = soup.find_all(href=re.compile("/phim/"))
    movies_list = list()

    for movie in movies:
        _movie = {}
        if movie.img:
            _movie["title"] = movie["title"]
            _movie["link"] = movie["href"]
            _movie["img"] = movie.img["data-src"]
            movies_list.append(_movie)
    return movies_list
        
def crawl_rating(URL):
    movies_list = crawl_moveek(URL)
    for i in range(len(movies_list)):
        movie = movies_list[i]
        soup = get_URL("https://moveek.com"+movie["link"])
        try:
            movie["gerne"] = soup.find(class_= "mb-0 text-muted text-truncate").string.strip().strip("-").strip()
            movie["description"] = soup.find(class_ = "mb-3 text-justify").text
            movie["rating"] = soup.find(href="/en/review/the-invisible-man/").text.strip()
        except:
            pass
    return movies_list

@app.route('/')
def index():
  data = crawl_rating(BASE_URL)
  return render_template('home.html',data=data)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 