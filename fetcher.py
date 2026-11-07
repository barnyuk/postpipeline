import asyncio
import analyzer
from aiohttp import ClientSession, ClientTimeout

url = 'https://jsonplaceholder.typicode.com/posts/'


async def fetch_post(session: ClientSession, post_id: int, semaphore: asyncio.Semaphore):
    async with semaphore:
        await logger(str(post_id))
        
        try: 
            
            async with session.get(f'{url}{post_id}') as response:

                response.raise_for_status()
                
                return await response.json()
        
        except asyncio.TimeoutError as e:  # noqa: UP041
            
            return f'TimeoutError для поста {post_id}: {e}'
        
        except Exception as e:  # noqa: BLE001
            
            return f'Exception для поста {post_id}: {e}'


async def logger(post_id: str) -> None:
    print(f"Начало загрузки поста {post_id}")


async def fetch_all_posts(num: int = 100, semaphore_count: int = 5, timeout: int = 5):
    semaphore = asyncio.Semaphore(semaphore_count)

    client_timeout = ClientTimeout(total=timeout)

    async with ClientSession(timeout=client_timeout) as session:

        tasks = [fetch_post(session, i, semaphore) for i in range(1, num + 1)]

        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    res = asyncio.run(fetch_all_posts(num=10))

res = analyzer.analyze_all_posts(res)



print(*res, sep='\n')
