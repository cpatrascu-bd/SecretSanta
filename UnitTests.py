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

def unit_test_create_group():

    print(client.create_group('poli','abc'))
    print(client.create_group('acs','abc'))

def unit_test_join_group():
    print(client.join_group_with_pass('poli','abc'))
    print(client.join_group_with_pass('acs','abc'))
    print(client.request_join_group('poli'))

def unit_test_get_groups():
    print(client.get_groups())

def unit_test_get_group():
    print(client.get_group('poli'))

def unit_test_templates():
    print(client.create_template('Template2', 'text_template2 pun si spatii'))
    print(client.get_templates())
    print(client.get_template('Template1'))

def unit_test_requests():
    print(client.request_join_group('poli'))


unit_test_create_user()
unit_test_login()
unit_test_create_group()
unit_test_join_group()
unit_test_get_groups()
unit_test_get_group()
unit_test_templates()