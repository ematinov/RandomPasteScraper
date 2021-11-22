import requests
import random
import time

from typing import List, Dict


ERROR_NO_CONNECTION = -1
ERROR_EMPTY_SERVER = -2



def process_json_request(r: requests.Request):
    if r.status_code == 200 and r.headers.get('content-type') == 'application/json':
        return r.json()

    return None


class PasteBin:
    url: str

    def __init__(self, url: str='http://localhost:8081'):
        self.url = url

    def insert_text(self, text: Dict[str, str]):
        r = requests.post(f"{self.url}/texts", json=text)

        return process_json_request(r)

    def get_indexes(self):
        r = requests.get(f"{self.url}/indexes")
        
        return process_json_request(r)

    def get_text(self, id: int):
        r = requests.get(f"{self.url}/texts/{id}")

        return process_json_request(r)


class RandomPasteBin(PasteBin):
    indexes: List[int] = None
    next_index_update: int = 0

    def update_indexes(self):
        cur_time = time.time()

        if cur_time <= self.next_index_update:
            return

        self.indexes = self.get_indexes()
        if self.indexes is not None:
            self.next_index_update = cur_time + 2*60

    def insert_text(self, text: Dict[str, str]):
        ret = super().insert_text(text)

        if ret is not None and self.indexes is not None:
            self.indexes['last_id'] = ret['id']

    def get_rand_text(self):
        self.update_indexes()

        if  self.indexes is None:
            return {'id': ERROR_NO_CONNECTION, 'text': 'PasteBin server is not available'}

        if self.indexes['first_id'] > self.indexes['last_id']:
            return {'id': ERROR_EMPTY_SERVER, 'text': 'PasteBin server is empty'}

        id = random.randint(self.indexes['first_id'], self.indexes['last_id'])

        ret = self.get_text(id)

        if ret is None:
            return {'id': ERROR_NO_CONNECTION, 'text': 'PasteBin server is not available'}

        return ret



if __name__ == "__main__":
    db = PasteBin()

    print(db.insert_text({"text": "some text"}))
    print(db.insert_text({"text": "some text 2"}))

    print(db.get_indexes())

    print(db.get_text(5))

    db = RandomPasteBin()

    print(db.insert_text({"text": "AAAA"}))
    print(db.get_rand_text())
    print(db.insert_text({"text": "BBBB"}))
    print(db.get_rand_text())

