import sqlite3
import os.path

# создаём таблицу
def CreateTable():
    if(not(os.path.exists('database.db'))):
        data = ReadAndParsingFile()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE logs
                    (date text, time text, key title,
                    ip title, subcat title, user_id title,
                    goods_id title, cart_id title, success_pay title,   
                    amount title)""")

        cursor.executemany("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?)", data)
        connection.commit()
    else:
        print('table has already exist')

def ReadAndParsingFile():
    listLines = []

#считываем файл и удаляем лишние элементы
    for line in open('logs.txt', 'r').readlines():
        element = line.strip().split(sep=' ')
        element.remove('shop_api')
        element.remove('|')
        element.remove('INFO:')
        del element[:5]
        tmp = element[4].split(sep='https://all_to_the_bottom.com/')[1].split('/')
        if '' in tmp: tmp.remove('')
        if tmp != []:
            if '?' in tmp[0]:
                firsttmp = tmp[0].split('?')
                secondtmp =  firsttmp[1].split('&')
                del firsttmp[1]
                firsttmp = secondtmp + firsttmp
                tmp = tmp + firsttmp
                del tmp[0]
            element[4] = tmp
        else:
            del element[4]

        listLines.append(element)

    for x in listLines:
        if len(x) == 5:
            if ((x[4][len(x[4])-1] == 'cart') or (x[4][len(x[4])-1] == 'pay')):
                del x[4][len(x[4])-1]

# оформляем список кортежей который потом пойдёт на вход базе данных,
# в пустые элементы будут иметь значение 'none'

    for x in listLines:
        if len(x) == 5:
            if  'user_id' in x[4][0]:
                y = x[4]
                del x[4]
                x.append('none')
                res = list()
                for i in y:
                    slice = i.split('=')
                    res.append(slice[1])
                x.append(res[0])
                x.append('none')
                x.append(res[1])
                x.append('none')
                x.append('none')
            elif 'goods_id' in x[4][0]:
                y = x[4]
                del x[4]
                x.append('none')
                res = list()
                for i in y:
                    slice = i.split('=')
                    res.append(slice[1])
                x.append('none')
                x.append(res[0])
                x.append(res[2])
                x.append('none')
                x.append(res[1])
            elif 'success_pay_' in x[4][0]:
                y = x[4]
                del x[4]
                x.append('none')
                res = list()
                for i in y:
                    slice = i.split('success_pay_')
                    res.append(slice[1])
                x.append('none')
                x.append('none')
                x.append('none')
                x.append(res[0])
                x.append('none')
            else:
                y = x[4]
                del x[4]
                res = ''
                for i in y:
                    res += i
                    res += '/'
                x.append(res)
                x.append('none')
                x.append('none')
                x.append('none')
                x.append('none')
                x.append('none')
        else:
            x.append('none')
            x.append('none')
            x.append('none')
            x.append('none')
            x.append('none')
            x.append('none')

    resList = []
    for line in listLines:
        resList.append(tuple(line))

    return resList

def main():
    CreateTable()