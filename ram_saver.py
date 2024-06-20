import asyncio
from typing import Any


class Receipt:
    def __init__(self, link: str, positions: list[dict[str, Any]]):
        self.link = link
        self.positions = positions
        self.our_positions = False
        self.partner_positions = False
        self.hz_positions = False

    def check(self, listings: dict, st_u: asyncio.Task):
        for position in self.positions:

            if position['name'] in listings['our']:
                self.our_positions = True
            elif position['name'] in listings['partner']:
                self.partner_positions = True
            elif position['name'] in listings['hz']:
                self.hz_positions = True
            else:
                st_u.cancel()
                result = False
                while not result:
                    match input(f'{position["name"]} - это?\n'
                                f'0 - Наше\n'
                                f'1 - Арендаторов\n'
                                f'2 - Хз\n'):
                        case '0':
                            self.our_positions = result = True
                            listings['our'].append(position["name"])
                        case '1':
                            self.partner_positions = result = True
                            listings['partner'].append(position["name"])
                        case '2':
                            self.hz_positions = result = True
                            listings['hz'].append(position["name"])


def dump_write(link: str, data: list[dict[str, Any]]):
    with open('dumpfile.txt', 'a') as f:
        f.write(link + '-|-' + "_|_".join([nm['name'].replace('\n', '') for nm in data]) + '\n')


def dump_read(i: int):
    with open('dumpfile.txt', 'r') as f:
        for k, line in enumerate(f):
            if k == i:
                link, sep, pnames = line.partition('-|-')
                position_names = [{'name': nm.replace('\n', '')} for nm in pnames.split('_|_')]
                return Receipt(link, position_names)
        return False
