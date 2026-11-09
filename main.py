import asyncio
import fetcher
import analyzer
import saver
from queue import Queue
from threading import Event
import time

start = time.time()

def run_pipeline():
    
    event = Event()
    q = Queue()
    
    result = asyncio.run(fetcher.fetch_all_posts(num=10, event=event))


    result = analyzer.analyze_all_posts(result)

    for post in result:
        q.put(post)

    saver.save_all_posts(q=q, event=event, all_posts=len(result))

 
def print_report(): 
    print(
    f"""=== Отчёт о работе пайплайна ===
    Запрошено постов: {fetcher.all_requested_posts}
    Успешно загружено: {fetcher.suc_loaded}
    Успешно обработано (CPU): {analyzer.suc_analyzed}
    Успешно сохранено (I/O): {saver.suc_saved}
    Общее время: {time.time() - start} сек."""
        )

if __name__ == '__main__':
    run_pipeline()

print_report()