#! python3

import smtplib
import random
import sys
import json

group_name = sys.argv[1]
student_file = sys.argv[2]
template_file = sys.argv[3]

students = []
sequence = []

email = 'SantaClaus334CB@gmail.com'
password = 'butelie123'
subject = '{} Secret Santa'.format(group_name)
phrase = '\n\nYour Secret Santa person is: '
body = ''


def get_file_content(file):
    # Retrieve json file content
    with open(file, 'r') as f:
        content = json.load(f)
    return content


def init():
    global students
    global body
    global sequence

    data = get_file_content(student_file)
    users = get_file_content('users/users.json')

    students = [(item['username'], item['email']) for item in users if item['username'] in data]
    body = get_file_content(template_file)[0]
    sequence = [i for i in range(len(students))]


def randomize():
    ok = 1
    while ok:
        ok = 0
        random.shuffle(sequence)
        for i in range(len(students)):
            if sequence[i] == i:
                ok = 1
                break


def send_email(target_email, picked_name):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
    except smtplib.SMTPException:
        print("Error while connecting to Gmail server ")
        return

    message = '\r\n'.join(['To: %s' % target_email, 'From: %s' % email, 'Subject: %s' % subject,
                           '', str(body) + str(phrase) + picked_name + '.'])

    try:
        server.sendmail(email, target_email, message)
        print('Email Sent to %s' % target_email)
    except smtplib.SMTPException:
        print('Error sending email to %s' % target_email)

    server.quit()


def main():
    init()
    randomize()

    for name, mail in students:
        send_email(mail, name)


main()
