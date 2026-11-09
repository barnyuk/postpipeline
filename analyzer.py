import hashlib
from math import sin
from multiprocessing import Process, Queue, Manager, Pool, Value, Lock
import queue

suc_analyzed = 0

def calculate_post_index(post: dict, q: Queue) -> dict:

    complexity_score = sum([sin(i) for i in range(1_000_000)])

    text = post['title'] + post['body']
    
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

    post['complexity_score'] = complexity_score

    post['text_hash'] = text_hash
    
    q.put(post['id'])
  
    return post

def consumer(q: Queue, value: Value) -> None: # type: ignore
    
    lock = Lock()
    
    while True:
        item = q.get()

        if item is None:
            break
        
        print(f'[Monitor] Пост {item} обработан.')
        
        with lock:
            value.value += 1

    

def analyze_all_posts(posts: list[dict]) -> None:

    with Manager() as manager:
        q = manager.Queue()
        value = Value('i', 0)
    
        process_consumer = Process(target=consumer, args=(q, value))
        process_consumer.start()
        
        try:
            with Pool() as pool:
                result = pool.starmap(calculate_post_index, [(post, q) for post in posts])
        finally:
            q.put(None)
            process_consumer.join()

        global suc_analyzed
        suc_analyzed = value.value
        
        print(f'Обработано постов: {value.value}')

    return result


