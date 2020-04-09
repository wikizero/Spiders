import re
import json
import time
from pprint import pprint
from urllib.parse import urljoin, urlsplit, urlparse

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


class DownloadTranscript():
    def __init__(self):
        self.conn = MongoClient('mongodb://localhost:27017/')
        self.db = self.conn.talks

    def get_page_url(self):
        start_url = 'https://www.ted.com/talks'
        res = requests.get(start_url)
        bs = BeautifulSoup(res.text, features="lxml")
        max_page = int([page.text for page in bs.select('.pagination a')][-2])
        print(f'max_page:{max_page}')

        for i in range(1, max_page + 1):
            url = f'https://www.ted.com/talks?page={i}'
            res = requests.get(url)
            bs = BeautifulSoup(res.text, features="lxml")
            for link in bs.select('#browse-results h4 .ga-link'):
                yield urljoin(url, link['href'])

    def get_comments(self, talk_id):
        url = f'https://www.ted.com/conversation_forums/{talk_id}?page=1&per_page=10&sort=rated'  # or sort by newest
        print(url)

    def get_transcript(self, talk_id):
        data = {}
        options = ['en', 'zh-cn']
        for opt in options:
            url = f'https://www.ted.com/talks/{talk_id}/transcript.json?language={opt}'
            try:
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    data[opt] = [''.join([p['text'].replace('\n', '') for p in line['cues']]) for line in
                                 res.json()['paragraphs']]
            except Exception:
                pass
        return data

    def get_detail(self, detail_url):
        data = {}
        try:
            res = requests.get(detail_url)
            bs = BeautifulSoup(res.text, features="lxml")

            # talk_id  <meta property="al:ios:url" content="ted://talks/59159?source=facebook" />
            talk_id_content = bs.select("meta[property$='al:ios:url']")[0]['content']
            talk_id = int(urlparse(talk_id_content).path[1:])

            data_spec = requests.get(f'https://www.ted.com/talks/{talk_id}/metadata.json').json()

            data['_id'] = talk_id
            data['desc'] = data_spec['description']
            data['tags'] = data_spec['talks'][0]['tags']
            data['title'] = data_spec['talks'][0]['title']
            data['video_views'] = data_spec['viewed_count']
            data['related_talks'] = [line['id'] for line in data_spec['talks'][0]['related_talks']]
            data['transcript'] = self.get_transcript(talk_id)

            print(talk_id)
            # insert or save
            self.db.raw.update({'_id': talk_id}, data, upsert=True)
        except Exception:
            pass

    def catch(self):
        for url in self.get_page_url():
            print(url)
            self.get_detail(url)
            time.sleep(3)


if __name__ == '__main__':
    # TODO 上传CSDN 基金数据
    dt = DownloadTranscript()
    detail_url = 'https://www.ted.com/talks/alexandra_auer_the_intangible_effects_of_walls_apr_2020'
    dt.get_detail(detail_url)
    # dt.catch()
