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


# Invalid arguments
send_message('AUTH')
# Account does not exist
send_message('AUTH andrei 123')
# Register account1
send_message('CREATE ACCOUNT andrei 123 andrei@yahoo.com')
# Register account1
send_message('CREATE ACCOUNT doru yolo andrei@gmail.com')
# Login as account1
status, token = send_message('AUTH andrei 123')
# Login as account 2
status1, token1 = send_message('AUTH doru yolo')


# Create 5 groups
send_message('CREATE GROUP grup1 pass1 {}'.format(token))
send_message('CREATE GROUP grup2 pass2 {}'.format(token))
send_message('CREATE GROUP grup3 pass3 {}'.format(token))
send_message('CREATE GROUP grup4 pass4 {}'.format(token))
send_message('CREATE GROUP grup5 pass5 {}'.format(token1))


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
send_message('REQUEST JOINP doru grup4 pass4 {}'.format(token1))
# Join invalid group
send_message('REQUEST JOINP doru grup6 pass1 {}'.format(token1))
# Resend join request
send_message('REQUEST JOINP doru grup4 pass4 {}'.format(token1))


# Request to join a group with password but wrong token
send_message('REQUEST JOIN doru grup1 {}'.format(token))
# Request to join invalid group
send_message('REQUEST JOIN andrei grup6 {}'.format(token))
# Request to join group with valid data
send_message('REQUEST JOIN doru grup2 {}'.format(token1))
send_message('REQUEST JOIN doru grup3 {}'.format(token1))
send_message('REQUEST JOIN andrei grup5 {}'.format(token))


# View all requests for invalid group
send_message('FETCH REQUESTS grup8{}'.format(token))
# View requests valid group
send_message('FETCH REQUESTS grup2{}'.format(token))


# Accept request, wrong admin
send_message('REQUEST ACCEPT doru grup2 {}'.format(token1))
# Accept request that does not exist
send_message('REQUEST ACCEPT andrei grup1 {}'.format(token))
# Accept valid request
send_message('REQUEST ACCEPT andrei grup5 {}'.format(token1))


# Deny request, wrong admin
send_message('REQUEST DENY doru grup2 {}'.format(token1))
# Deny request that does not exist
send_message('REQUEST DENY doru grup1 {}'.format(token1))
# Deny valid request
send_message('REQUEST DENY doru grup2 {}'.format(token))


# Unjoin when user != token
send_message('REQUEST UNJOIN andrei grup5 {}'.format(token1))
# Unjoin user that was not in group
send_message('REQUEST UNJOIN andrei grup3 {}'.format(token))
# Unjoin user from invalid group
send_message('REQUEST UNJOIN andrei grup7 {}'.format(token))
# Valid unjoin reuqest
send_message('REQUEST UNJOIN andrei grup5 {}'.format(token))


# Delete group, wrong admin
send_message('DELETE GROUP grup1 {}'.format(token1))
# Delete invalid group
send_message('DELETE GROUP grup8 {}'.format(token))
# Delete group
send_message('DELETE GROUP grup1 {}'.format(token))


# Logout invalid token
send_message('LOGOUT {}'.format('abc'))
# Log both users out
send_message('LOGOUT {}'.format(token1))
send_message('LOGOUT {}'.format(token))
