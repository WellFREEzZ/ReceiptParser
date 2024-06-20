import asyncio
import json
import os

import html_parser
import ram_saver


async def prepare_status():
    while True:
        print('Парсим чеки')
        await asyncio.sleep(1)
        print('Парсим чеки.')
        await asyncio.sleep(1)
        print('Парсим чеки..')
        await asyncio.sleep(1)
        print('Парсим чеки...')
        await asyncio.sleep(1)


async def parse_receipts(loop: asyncio.AbstractEventLoop):
    fp = open('input.txt', 'r')
    timer = loop.create_task(prepare_status())
    myline = fp.readline().replace("\n", "")
    while myline:
        await html_parser.parse(myline)
        myline = fp.readline()
    fp.close()
    timer.cancel()


def marking_activity():
    i = 0
    with open('output.csv', 'w') as f:
        f.write(f'Ссылка на чек;Наш;Арендаторов\n')

    cur_receipt = ram_saver.dump_read(i)
    while cur_receipt:
        listings = json.load(open('listings.dmp', 'r'))
        print(listings)
        cur_receipt.check(listings)

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


async def main():
    if os.path.exists('output.csv'):
        os.remove('output.csv')
    match input('Загрузить чеки заново?\nY-да\n[AnyOther]-нет\n').lower():
        case 'y':
            if os.path.exists('dumpfile.txt'):
                os.remove('dumpfile.txt')
            await parse_receipts(asyncio.get_event_loop())
    marking_activity()


if __name__ == '__main__':
    asyncio.run(main())
