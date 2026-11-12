import time
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from queue import Queue
from threading import Event, Lock, Thread

suc_saved = 0

def save_post(post_data: dict | None, lock: Lock) -> None:
    global suc_saved

    if post_data is None:
        return

    with lock:

        with open('results.log', 'a', encoding='utf-8') as file:
            file.write(f'id: {post_data['id']}, title: {post_data['title']}\n')

        suc_saved += 1
    time.sleep(0.05)



def print_progress(event: Event) -> None:

    while event.is_set():
        print(f'Прогресс сохранения: {suc_saved} / {all}')
    

def get_item_from_queue(q: Queue) -> Generator[dict, None, None]:
    yield q.get()


def save_all_posts(q, event: Event) -> None:

    lock = Lock()

    progress = Thread(target=print_progress, args=(event, ))
    progress.start()

    
    with ThreadPoolExecutor(max_workers=4) as executor:
        
        list(executor.map(partial(save_post, lock=lock), get_item_from_queue(q=q)))
        executor.shutdown(wait=True)
    
    event.set()

    