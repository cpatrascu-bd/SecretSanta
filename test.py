import socket


def send_message(command):
    sock = socket.socket()
    sock.connect(('127.0.0.1', 9001))

    sock.send(bytes(command.encode('utf-8')))
    data = (sock.recv(4096).decode('utf-8')).split(' ')
    stat = data[0]
    tok = " ".join([x for x in data[1:]])
    print(stat, tok)
    sock.close()

    return stat, tok

send_message('AUTH')
# Account does not exist
send_message('AUTH andrei 123')
# Register account1
send_message('CREATE ACCOUNT andrei 123 andrei@yahoo.com')
# Register account1
send_message('CREATE ACCOUNT doru yolo andrei@gmail.com')
# Login as account1
status, token = send_message('AUTH andrei 123')
#Login as account 2
status1, token1 = send_message('AUTH doru yolo')


# Create 2 groups
send_message('CREATE GROUP grup1 pass1 {}'.format(token))
send_message('CREATE GROUP grup2 pass2 {}'.format(token))
# Create 2 templates
send_message('CREATE TEMPLATE temp1 {} ana are multe mere'.format(token))
send_message('CREATE TEMPLATE temp2 {} mario yolo'.format(token))


# Get all groups and templates
send_message('FETCH GROUPS {}'.format(token))
send_message('FETCH TEMPLATES {}'.format(token))
# Fetch specific group or template
send_message('FETCH GROUP grup2 {}'.format(token))
send_message('FETCH TEMPLATE temp1 {}'.format(token))


# Join a group with password but wrong token
send_message('REQUEST JOINP doru grup1 pass1 {}'.format(token))
# Join a group with wrong password
send_message('REQUEST JOINP andrei grup1 pass2 {}'.format(token))
# Join group with correct password
send_message('REQUEST JOINP andrei grup1 pass1 {}'.format(token))
# Join invalid group
send_message('REQUEST JOINP doru grup3 pass1 {}'.format(token1))
# Resend join request
send_message('REQUEST JOINP andrei grup1 pass1 {}'.format(token))


# Request to join a group with password but wrong token
send_message('REQUEST JOIN doru grup1 {}'.format(token))
# Request to join invalid group
send_message('REQUEST JOIN andrei grup3 {}'.format(token))
# Request to join group with valid data
send_message('REQUEST JOIN andrei grup2 {}'.format(token))
send_message('REQUEST JOIN doru grup2 {}'.format(token1))


# Accept request, wrong admin
send_message('REQUEST ACCEPT doru grup2 {}'.format(token1))
# Accept request that does not exist
send_message('REQUEST ACCEPT andrei grup1 {}'.format(token))
# Accept valid request
send_message('REQUEST ACCEPT andrei grup2 {}'.format(token))


# Deny request, wrong admin
send_message('REQUEST DENY doru grup2 {}'.format(token1))
# Deny request that does not exist
send_message('REQUEST DENY doru grup1 {}'.format(token1))
# Deny valid request
send_message('REQUEST DENY doru grup2 {}'.format(token))