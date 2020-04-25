#! python3

import smtplib
import random
import json

SUCCESS = 1
FAIL = 0

students = []
sequence = []

email = 'SantaClaus334CB@gmail.com'
password = 'butelie123'
subject = 'Secret Santa Results'
error_subject = 'Error while sending emails for Secret Santa'
phrase = '\n\nYour Secret Santa person is: '
ante_body = 'Group: '
body = ''


def get_file_content(file):
    # Retrieve json file content
    with open(file, 'r') as f:
        content = json.load(f)
    return content


def init(student_file, template_file):
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


def send_email(target_email, sub, text):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
    except smtplib.SMTPException:
        return FAIL, 'Error while connecting to Gmail server'

    message = '\r\n'.join(['To: {}'.format(target_email),
                           'From: {}'.format(email),
                           'Subject: {}'.format(sub),
                           '', text])

    try:
        server.sendmail(email, target_email, message)
    except smtplib.SMTPException:
        server.quit()
        return FAIL, 'Error while sending email to {}'.format(target_email)

    server.quit()
    return SUCCESS, 'Email sent to user'


def run(group_name, student_file, template_file, admin_email):
    init(student_file, template_file)
    randomize()

    err_body = ''
    cnt = 0
    for i in range(len(students)):
        name, mail = students[i]
        code, err = send_email(mail, subject, ''.join([ante_body, group_name, '\n\n', body,
                               phrase, students[sequence[i]][0], '.']))
        if code == FAIL:
            err_body += '\n\n Error {}:\n.{}'.format(str(cnt), err)
            cnt += 1

    if err_body:
        send_email(admin_email, error_subject,  err_body)
