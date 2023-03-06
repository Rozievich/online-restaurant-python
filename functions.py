import json
from datetime import datetime
import bcrypt


def hashing(data):  # noqa
    data = data.encode('ASCII')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(data, salt)
    hashed = hashed.decode('ASCII')
    return hashed


def hashing_read(data, password):
    data = data.encode('ASCII')
    password = password.encode('ASCII')
    if bcrypt.checkpw(password, data):
        return True
    else:
        return False


class File:  # noqa
    def __init__(self, filename):  # noqa
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as file:
            try:
                data = json.load(file)
            except:  # noqa
                data = []
        return data

    def write(self, page):
        with open(self.filename, 'w') as file:
            json.dump(page, file, indent=3)


def admin(data):
    if data == 'admin':
        return True
    else:
        return False


class User:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = hashing(password)
        self.admin = admin(username)
        self.products = []
        self.drinks = []

    def register(self):
        obj = File('user.json')
        list_ = obj.read()
        list_.append(self.__dict__)
        obj.write(list_)

    def check_user(self):
        obj = File('user.json')
        list_ = obj.read()
        for i in list_:
            if i['username'] == self.username:
                return False
        else:
            return True

    def login(self, password):
        obj = File('user.json')
        func = obj.read()
        for i in func:
            if i['username'] == self.username and hashing_read(i['password'], password):
                return True
        else:
            return False

    def check_admin(self):
        obj = File('user.json')
        request = obj.read()
        for i in request:
            if i['username'] == self.username:
                return i['admin']
        else:
            return False

    def add_admin(self, username):  # noqa
        obj = File('user.json')
        request = obj.read()
        for i in request:
            if i['username'] == username:
                i['admin'] = True
                obj.write(request)
                return True
        else:
            return False

    def add_product(self, order, count):
        obj = File('user.json')
        lists = obj.read()
        order['count'] = count
        time = datetime.now()
        order['time'] = time.strftime('%Y:%m:%d %H:%M')
        for i in lists:
            if i['username'] == self.username:
                i['products'].append(order)
                break
        obj.write(lists)

    def my_products(self):  # noqa
        obj = File('user.json')
        request_ = obj.read()
        _list = []
        for i in request_:
            if i['username'] == self.username:
                for j in i['products']:
                    _list.append({"name": j['name'], "time": j['time'], "count": j['count']})
                for j in i['drinks']:
                    _list.append({"name": j['name'], "time": j['time'], "count": j['count']})
        return _list

    def report(self):  # noqa
        obj = File('user.json')
        response = obj.read()
        summa = 0
        for i in response:
            if i['username'] == self.username:
                for j in i['products']:
                    summa += j['price'] * int(j['count'])
                for j in i['drinks']:
                    summa += j['price'] * int(j['count'])
        return summa

    def drink_products(self, order, count):
        obj = File('user.json')
        response = obj.read()
        order['count'] = count
        time = datetime.now()
        order['time'] = time.strftime('%Y:%m:%d %H:%M')
        for i in response:
            if i['username'] == self.username:
                i['drinks'].append(order)
                break
        obj.write(response)

    def current_order(self):
        obj = File('user.json')
        response = obj.read()
        data = datetime.now()
        list_ = []
        for i in response:
            if i['username'] == self.username:
                for j in i['products']:
                    now_time = j['time'].split(' ', 1)
                    if now_time[0] == str(data.strftime("%Y:%m:%d")):
                        list_.append(j)
                for j in i['drinks']:
                    now_time = j['time'].split(' ', 1)
                    if now_time[0] == str(data.strftime("%Y:%m:%d")):
                        list_.append(j)
        return list_


class Food:
    def __init__(self, name=None, price=None):
        self.name = name
        self.price = price

    def add_food(self):
        obj = File('menu.json')
        info = obj.read()
        try:
            info[0]['foods'].append(self.__dict__)
        except:  # noqa
            info.append({'foods': [self.__dict__], 'drinks': []})
        obj.write(info)

    def check_food(self, name):  # noqa
        obj = File('menu.json')
        info = obj.read()
        for i in info:
            for j in i['foods']:
                if j['name'] == name:
                    return True
            else:
                return False

    def check_drink(self, name):  # noqa
        obj = File('menu.json')
        info = obj.read()
        for i in info:
            for j in i['drinks']:
                if j['name'] == name:
                    return True
            else:
                return False

    def add_drink(self):
        obj = File('menu.json')
        info = obj.read()
        try:
            info[0]['drinks'].append(self.__dict__)
        except:  # noqa
            info.append({'foods': [], 'drinks': [self.__dict__]})
        obj.write(info)

    def drink_menu(self):  # noqa
        obj = File('menu.json')
        info = obj.read()
        for i in info:
            for j in i['drinks']:
                print(f'Name: {j["name"]}\nPrice: {j["price"]}\n<--------------->')

    def food_menu(self):  # noqa
        obj = File('menu.json')
        info = obj.read()
        for i in info:
            for j in i['foods']:
                print(f'Name: {j["name"]}\nPrice: {j["price"]}\n<--------------->')
