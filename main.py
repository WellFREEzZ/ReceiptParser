import asyncio
import json
import os

import html_parser
import ram_saver
import logging

logging.basicConfig(level=logging.WARNING)


async def update_status(status: str):
    while True:
        for i in range(4):
            print(status + i * '.', flush=True)
            await asyncio.sleep(0.5)


async def parse_receipts(loop: asyncio.AbstractEventLoop):
    fp = open('input.txt', 'r')
    timer = loop.create_task(update_status('Парсим чеки'))
    tasks = []
    myline = fp.readline().replace("\n", "")
    while myline:
        while len(tasks) < 100:  # Careful, semaphore!
            tasks.append([loop.create_task(html_parser.parse(myline)), 0])
            myline = fp.readline().replace("\n", "")

        await asyncio.sleep(0.002)

        for task in tasks:
            if task[0].done():
                if exc := task[0].exception():
                    logging.error(msg='Error! Retrying...', exc_info=exc)
                    if stack := task[0].get_stack():
                        ln = stack[0].f_locals.get("myline")
                        if task[1] < 5:
                            tasks.append([loop.create_task(html_parser.parse(ln)), task[1] + 1])
                        else:
                            with open('failed.txt', 'a') as f:
                                f.write(ln + '\n')
                tasks.remove(task)

    fp.close()
    await asyncio.wait([t[0] for t in tasks])
    timer.cancel()


async def marking_activity(loop: asyncio.AbstractEventLoop):
    i = 0
    status_updater = loop.create_task(update_status('Размечаем'))
    with open('output.csv', 'w') as f:
        f.write(f'Ссылка на чек;Наш;Арендаторов\n')

    cur_receipt = ram_saver.dump_read(i)
    while cur_receipt:
        await asyncio.sleep(0.002)
        listings = json.load(open('listings.dmp', 'r'))
        cur_receipt.check(listings, status_updater)
        if status_updater.cancelled():
            status_updater = loop.create_task(update_status('Размечаем'))
        match cur_receipt.our_positions, cur_receipt.partner_positions, cur_receipt.hz_positions:
            case False, False, False:
                our_status = partner_status = "Ошибка, давай ручками"
            case False, False, True:
                our_status = partner_status = "Возможно"
            case False, True, False:
                our_status, partner_status = "Нет", "Да"
            case False, True, True:
                our_status, partner_status = "Возможно", "Да"
            case True, False, False:
                our_status, partner_status = "Да", "Нет"
            case True, False, True:
                our_status, partner_status = "Да", "Возможно"
            case True, True, False:
                our_status, partner_status = "Да", "Да"
            case True, True, True:
                our_status, partner_status = "Да", "Да"

        with open('output.csv', 'a') as f:
            f.write(f'{cur_receipt.link};{our_status};{partner_status}\n')
        i += 1
        cur_receipt = ram_saver.dump_read(i)
        json.dump(listings, open('listings.dmp', 'w'))
    if not status_updater.cancelled():
        status_updater.cancel()


async def main():
    loop = asyncio.get_event_loop()
    if os.path.exists('output.csv'):
        os.remove('output.csv')

    if os.path.exists('dumpfile.txt'):
        match input('Загрузить чеки заново?\nY-да\n[AnyOther]-нет\n').lower():
            case 'y':
                os.remove('dumpfile.txt')

    if os.path.exists('listings.dmp'):
        match input('Сбросить листинги?\nY-да\n[AnyOther]-нет\n').lower():
            case 'y':
                os.remove('listings.dmp')

    if not os.path.exists('dumpfile.txt'):
        await parse_receipts(loop)

    if not os.path.exists('listings.dmp'):
        init_listing = {'our': [], 'partner': [], 'hz': []}
        json.dump(init_listing, open('listings.dmp', 'w'))

    await marking_activity(loop)
    print('Готово!')


if __name__ == '__main__':
    asyncio.run(main())
