from client import Client
import os
client = Client()


def unit_test_create_user():
    try:
        os.remove('utilizatori.json')
    except:
        print("utilizatori.json does not exist")
    print(client.create_user('cristi','cristi', 'a@b.c'))
    print(client.create_user('cristi', 'cristi', 'a@b.c'))
    print(client.create_user('cristi2', 'cristi', 'a@b.c'))
    print(client.create_user('vlad', 'vladut', 'vlad@yahoo'))
    print(client.create_user('vlad', 'vladut', 'vlad@yahoo.'))
    print(client.create_user('andrei', 'an', 'a@gmail.com'))
    print(client.create_user('a','andrei','c'))


def unit_test_login():
    print(client.login('cristi', 'cristi'))
    print(client.login('cristi2', 'cristi'))
    print(client.login('cristi', 'cristi2'))


unit_test_create_user()
unit_test_login()