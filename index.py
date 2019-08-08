from flask import Flask, render_template
from bs4 import BeautifulSoup
import urllib, json

kcci = Flask(__name__)

@kcci.route('/')
def get_stories():
    main = urllib.request.urlopen('https://kcci.com')
    soup = BeautifulSoup(main, 'html.parser')
    data = soup.find(id='json-ld').text.replace('\n','')
    jdata = json.loads(data)

    payload = {}
    count = 0
    for story in jdata['itemListElement']:
        # There are only 6 local stories at one time
        if count > 6:
            return render_template('index.html', payload=payload)
        
        story = urllib.request.urlopen(story['url'])
        soup = BeautifulSoup(story, 'html.parser')
        data = soup.find(id='json-ld').text.replace('\n','')
        storyobj = json.loads(data)

        # Get info from story
        title = storyobj['name']
        date = storyobj['datePublished'][:10] + ' @ ' +storyobj['datePublished'][11:19]
        link = storyobj['url']
        # Try to get text, otherwise get transcript
        try:
            body = storyobj['articleBody']
        except KeyError:
            body = storyobj['video']['transcript']

        payload[title] = body
        count = count + 1

if __name__ == '__main__':
    kcci.run()