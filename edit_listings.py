import json

test = json.load(open('listings.dmp', 'r'))

for k, v in test.items():
    print(f'{k}:')
    for val in v:
        print(f'  {val}')

cate = None
match input('\nЧто меняем?\n'
            '0 - our\n'
            '1 - parner\n'
            '2 - hz\n'):
    case '0':
        cate = 'our'
    case '1':
        cate = 'partner'
    case '2':
        cate = 'hz'

if cate is None:
    exit()

print()
for i, v in enumerate(test[cate]):
    print(f'{i}: {v}')


index = int(input('Номер?\n'))

send_to = int(input(test[cate][index] + ' куда перемещаем?\n' + '\n'.join(
    f"{i} - {cats}" for i, cats in enumerate(test.keys())) + '\n'))

if input('\nПодтверждаем перемещение ' + (test[cate][index]) + ' из ' +
         cate + ' в ' + list(test.keys())[send_to] + '\nНапиши YES\n').lower() == 'yes':
    test[list(test.keys())[send_to]].append(test[cate][index])
    del (test[cate][index])
    print()
    for k, v in test.items():
        print(f'{k}:')
        for val in v:
            print(f'  {val}')

    json.dump(test, open('listings.dmp', 'w'))

