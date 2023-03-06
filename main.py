from functions import File, User, Food


def login_menu(ob, is_admin):
    if not is_admin:
        while True:
            print('<---------------------->')
            print('1) New Order: \n2) New Drink: \n3) My Orders: \n4) Current orders: \n5) Report: \n6) Logout: ')
            order = input('>>> ')
            if order == '1':
                product = File('menu.json')
                nativ = product.read()  # noqa
                for i in nativ:
                    for j in i['foods']:
                        print('<---------------------->')
                        print(f'Name: {j["name"]}\nPrice: {j["price"]}')
                print('<---------------------->')
                prod = input('Product name: ').title()
                count = input('Count: ')
                try:
                    count = int(count)
                except:  # noqa
                    print('Wrong answer!\n')
                    continue
                else:
                    if count >= 0:
                        for i in nativ:
                            for j in i['foods']:
                                if j['name'] == prod:
                                    ob.add_product(j, count)
                                    print('Job Done!\n')
                                    break
                            break
                        else:
                            print('Food not found!\n')
                    else:
                        print('Wrong answer!\n')
            elif order == '2':
                product = File('menu.json')
                nativ = product.read()  # noqa
                for i in nativ:
                    for j in i['drinks']:
                        print('<---------------------->')
                        print(f'Name: {j["name"]}\nPrice: {j["price"]}')
                print('<---------------------->')
                prod = input('Product name: ').title()
                count = input('Count: ')
                try:
                    count = int(count)
                except:  # noqa
                    print('Wrong answer!')
                else:
                    if count >= 0:
                        for i in nativ:
                            for j in i['drinks']:
                                if j['name'] == prod:
                                    ob.drink_products(j, count)
                                    print('Job Done!\n')
                                    break
                            break
                        else:
                            print('Drink not found!\n')
                    else:
                        print('Wrong answer!')
            elif order == '3':
                response = ob.my_products()
                print('Your Orders!\n')
                for i in response:
                    print(f"Name: {i['name']}\nTime: {i['time']}\nCount: {i['count']}\n<---------------------->")
                print('\nJob Done!\n')
            elif order == '4':
                main_data = ob.current_order()
                summa = 0
                print('Current order!\n<---------------------->')
                for i in main_data:
                    print(f'Name: {i["name"]}\nPrice: {i["price"]}\nCount: {i["count"]}\n<---------------------->')
                    summa += i['price'] * int(i['count'])
                print(f'Current report: {summa}')
            elif order == '5':
                repo = ob.report()
                print(f"Your Report: {repo}")
                print('Job Done!\n')
            elif order == '6':
                main()
                break
            else:
                print('No such section exists!\n')
    else:
        print('\nAdmin Page!\n')
        while True:
            print('1) Drinks Menu: \n2) Foods Menu: \n3) Add food: \n4) Add drink: \n5) Add admin: \n6) Exit: ')
            response = input('>>> ')
            if response == '1':
                print('Drink Menu!\n<------------>')
                Food().drink_menu()
            elif response == '2':
                print('Food Menu!\n<------------>')
                Food().food_menu()
            elif response == '3':
                print('Add food page!\n')
                name = input('Name: ').title()
                price = int(input("Price: "))
                if price >= 0:
                    foods = Food(name, price)
                    hint = foods.check_food(name)
                    if not hint:
                        foods.add_food()
                        print('Job Done!\n')
                    else:
                        print('This dish is available to you!\n')
                else:
                    print('Wrong answer!\n')
            elif response == '4':
                print('Add drink page!\n')
                name = input('Name: ').title()
                price = int(input('Price: '))
                if price >= 0:
                    drinks = Food(name, price)
                    hint = drinks.check_drink(name)
                    if not hint:
                        drinks.add_drink()
                        print('Job Done!\n')
                    else:
                        print('This dish is available to you!\n')
                else:
                    print("Wrong answer!\n")
            elif response == '5':
                username = input('Username: ')
                user = ob.add_admin(username)
                if user:
                    print('Job Done!\n')
                else:
                    print('No such username!\n')
            elif response == '6':
                print('Main Menu!\n')
                main()
                break
            else:
                print('No such section exists!')
                main()
                break


def main():
    print('\nRestaurant!\n')
    print('1) Login: \n2) SignUp: \n3) Exit: ')
    repost = input('>>> ')
    if repost == '1':
        print('<---------------------->')
        print('Login Page!')
        user = input('Username: ')
        password = input('Password: ')
        ob = User(user, password)
        request = ob.login(password)
        is_admin = ob.check_admin()
        if request:
            login_menu(ob, is_admin)
        else:
            print("Wrong Username!")
            main()
    elif repost == '2':
        print('<---------------------->')
        print('Register Page!')
        username = input('Username: ')
        password = input('Password: ')
        obj = User(username, password)
        chesk = obj.check_user()  # noqa
        if chesk:
            obj.register()
            print('Welcome to the system!')
            main()
        else:
            print('This username has been used before!')
            main()
    elif repost == '3':
        print('Logout was successful!')
        return
    else:
        print('No such section exists!')
        main()


main()
