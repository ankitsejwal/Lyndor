import urllib2
import re
from bs4 import BeautifulSoup

def create_soup(urlink):
    url = urllib2.urlopen(urlink)
    pg_content = url.read()
    return BeautifulSoup(pg_content, 'lxml')

def save_chapters(urlink):
    soup = create_soup(urlink)
    heading4 = soup.find_all('h4', {"class": "ga"})

    chapter_no = 0
    for h in heading4:
        chapter = h.text
        chapter = re.sub('[^a-zA-Z0-9.]', ' ', chapter)

        if chapter[1] == '.' or chapter[2] == '.':
            for c in range(len(chapter)):
                if chapter[c] == '.':
                    chapter_name =  chapter[c+2:]
                    print str(chapter_no) + ". " +chapter_name
                    chapter_no += 1
        else:
            print str(chapter_no) + ". " +chapter
            chapter_no += 1
  
if __name__ == '__main__':
    urlink = "https://www.lynda.com/Dreamweaver-tutorials/Dreamweaver-CS6-Essential-Training/97613-2.html?srchtrk=index%3a3%0alinktypeid%3a2%0aq%3adreamweaver+essentials%0apage%3a1%0as%3arelevance%0asa%3atrue%0aproducttypeid%3a2"
    save_chapters(urlink)
