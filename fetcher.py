import asyncio

from aiohttp import ClientSession

url = 'https://jsonplaceholder.typicode.com/posts/'


async def fetch_post(session: ClientSession, post_id, semaphore: asyncio.Semaphore):

    async with semaphore:  # noqa: SIM117
        async with session.get(f'{url}{post_id}') as response:
            try:
                response.raise_for_status()

                return await response.json()
            except TimeoutError as e:
                
                return f'asyncio.TimeoutError: {e}'
            except Exception as e:  # noqa: BLE001
                return f'Exception: {e}'


async def logger(string: str) -> None:
    print(string)


async def fetch_all_posts(num: int = 100, semaphore_count = 5, timeout: int = 5):
    
    semaphore = asyncio.Semaphore(semaphore_count)

    async with ClientSession(timeout=timeout) as session:
        tasks = [fetch_post(session, i, semaphore) for i in range(1, num + 1)]
        log_task = asyncio.create_task(logger('start'))
        
        return await asyncio.gather(*tasks, log_task)

print(asyncio.run(fetch_all_posts(num = 10)))

