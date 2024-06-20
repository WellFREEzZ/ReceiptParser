from typing import List, Dict, Any

from bs4 import BeautifulSoup
import aiohttp
import asyncio

import ram_saver


async def parse(link):
    final_data = []

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(
                link) as resp:
            txt = await resp.text()
            await session.close()

    reicept = BeautifulSoup(txt, 'html.parser').find('div', id='fido_cheque_container')
    content = BeautifulSoup(reicept.text, 'html.parser')

    r_body = content.find('table').find_next_sibling('table').table.table.find('tr').find_next_sibling('tr').tr.td

    for r in r_body.find_all('span', recursive=False):
        tbls = r.tr.td.find_all('table', recursive=False)
        t1_span = tbls[1].tr.td.span.b.find_all('span', recursive=False)
        final_data.append({
            'name': tbls[0].tr.td.span.b.text[tbls[0].tr.td.span.b.text.index(': ')+2:],
            'count': t1_span[0].text,
            'coast': t1_span[2].text,
            'price': tbls[2].tr.find_all('td', recursive=False)[1].span.text
        })

    ram_saver.dump_write(link, final_data)


if __name__ == '__main__':
    asyncio.run(
        parse('https://lk.platformaofd.ru/web/noauth/cheque/id?id=88585559402&date=1679862449000&fp=1950027559'))
