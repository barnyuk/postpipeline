import asyncio
from aiohttp import ClientSession, ClientTimeout
from threading import Event

url = 'https://jsonplaceholder.typicode.com/posts/'

all_requested_post, suc_loaded = 0, 0

async def fetch_post(session: ClientSession, post_id: int, semaphore: asyncio.Semaphore, event: Event):
    global suc_loaded 
    async with semaphore:
        await logger(str(post_id), event)
        
        try: 
            
            async with session.get(f'{url}{post_id}') as response:

                response.raise_for_status()
                suc_loaded += 1
                
                return await response.json()
        
        except asyncio.TimeoutError as e:  # noqa: UP041
            
            return f'TimeoutError для поста {post_id}: {e}'
        
        except Exception as e:  # noqa: BLE001
            
            return f'Exception для поста {post_id}: {e}'


async def logger(post_id: str, event: Event) -> None:
    print(f"Начало загрузки поста {post_id}")
    
    if not event.is_set():
        return


async def fetch_all_posts(event: Event, num: int = 100, semaphore_count: int = 5, timeout: int = 5) -> list[dict]:
    global all_requested_posts
    all_requested_posts = num
    
    semaphore = asyncio.Semaphore(semaphore_count)

    client_timeout = ClientTimeout(total=timeout)

    async with ClientSession(timeout=client_timeout) as session:

        tasks = [fetch_post(session, i, semaphore, event) for i in range(1, num + 1)]

        return await asyncio.gather(*tasks)




