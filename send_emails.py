#! python3

import smtplib
import random
import json


students = []
sequence = []

email = 'SantaClaus334CB@gmail.com'
password = 'butelie123'
subject = 'Secret Santa'
phrase = '\n\nYour Secret Santa person is: '
body = ''


def get_file_content(file):
    # Retrieve json file content
    with open(file, 'r') as f:
        content = json.load(f)
    return content


def init(group_name, student_file, template_file):
    global students
    global body
    global sequence
    global subject

    data = get_file_content(student_file)
    users = get_file_content('users/users.json')

    students = [(item['username'], item['email']) for item in users if item['username'] in data]
    subject = group_name + subject
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
        return 'FAIL'

    message = '\r\n'.join(['To: %s' % target_email, 'From: %s' % email, 'Subject: %s' % subject,
                           '', str(body) + str(phrase) + picked_name + '.'])

    try:
        server.sendmail(email, target_email, message)
    except smtplib.SMTPException:
        server.quit()
        return 'FAIL'

    server.quit()
    return 'SUCCESS'


def run(group_name, student_file, template_file):
    init(group_name, student_file, template_file)
    randomize()

    for name, mail in students:
        if send_email(mail, name) == 'FAIL':
            return 'FAIL'

    return 'SUCCESS'
