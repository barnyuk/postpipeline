import hashlib
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from math import sin
from multiprocessing import Process, Queue


def calculate_post_index(post: dict, q: Queue) -> dict:
    complexity_score = sum([sin(i) for i in range(1_000_000)])

    text = post['title'] + post['body']
    
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

    post['complexity_score'] = complexity_score

    post['text_hash'] = text_hash
    q.put(post['post_id'])

    return post

def consumer(q: Queue) -> None:
    while True:
        item = q.get()

        if item is None:
            break
        
        print(print(f'[Monitor] Пост {item} обработан.'))

def analyze_all_posts(posts: list[dict]) -> None:
    q = Queue()
    
    target = partial(calculate_post_index, q=q)
    process_consumer = Process(target=consumer, args=(q,))
    process_consumer.start()

    with ProcessPoolExecutor(max_workers=4) as executor:
        result = list(executor.map(target, posts))

    return result


