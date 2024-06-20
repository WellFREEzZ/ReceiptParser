import asyncio


async def update_status(status: str):
    while True:
        for i in range(4):
            print(status + i * '.')
            await asyncio.sleep(1)


async def main():
    loop = asyncio.get_event_loop()
    status_activity = loop.create_task(update_status('test'))
    await asyncio.sleep(10)
    status_activity.cancel()
    await asyncio.sleep(10)
    status_activity.uncancel()
    await asyncio.sleep(20)
    status_activity.cancel()

if __name__ == '__main__':
    asyncio.run(main())
