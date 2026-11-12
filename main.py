import asyncio
import time
from threading import Event

import analyzer
import fetcher
import saver

start = time.time()

def run_pipeline():
    
    event = Event()
    
    result = analyzer.analyze_all_posts(
        asyncio.run(fetcher.fetch_all_posts(num=10, event=event))
    )

    saver.save_all_posts(q=result, event=event)

 
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