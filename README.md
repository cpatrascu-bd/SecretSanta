# SecretSanta

![Secret_Santa_Project](https://user-images.githubusercontent.com/47899873/80345500-dd145280-8871-11ea-99ac-b83794ea6d8a.jpg)

## Description & Purpose

On Christmas, many groups of friends or coleagues organize Secret Santa events.

Usually, organizing a Secret Santa requires all participants to assemble, make name tickets and everyone to pick a ticket.

Sometimes, this goal can be hard to achive, because it is hard to assemble a large group of people.
Also, using the traditional way, some people find out who will give them a gift.

This is where our application intervenes.
Using this project, users will be able to form SecretSanta groups. 
When the group admin decides , the application, for each member group, will radomly select who he will have to give the gift.
This information will be send by email.


## Features

- Compatible to Linux and Windows client systems
- You can create and manage Secret Santa groups
- You can create templates for the email text
- You can send automatically and randomly pair people from a group and send them the pairing result

## Requirements

- At least 1GB RAM and i3 4th series
- Python3.7 or above
- The following python modules(only for manual build):
	- PyQt5
- Internet connection

## Installation

### Binary release
Simply download the binary files for your operating system and run them.

### Script release
- `sudo apt-get update`
- `sudo apt-get install -y python3.8  python3-pip`
- `pip install PyQt5`
- `git clone https://github.com/cristi799/SecretSanta`
- `cd SecretSanta && python server.py && python auth.exe`

Enjoy!
	
## Usage

###### Server
For the server side, you have to run server.py or the server executable.

###### Client
You will have to run auth.py or the SecretSanta executable.
This will prompt a login window.
Here you can create an account that will be stored on server.

![login](https://user-images.githubusercontent.com/47899873/80350739-da1d6000-8879-11ea-9582-bc60324b41db.png)


After that, you can login. Now the dashboard will be prompted.

![dashboard](https://user-images.githubusercontent.com/47899873/80350899-15b82a00-887a-11ea-842c-9774fb095f9b.png)

Here you have 4 options:
	Create Group
	View Groups
	Create Template
	View Templates

Create Group: 

![create_group](https://user-images.githubusercontent.com/47899873/80351035-53b54e00-887a-11ea-99bb-51ba4276ee47.png)

View Groups:

![view_groups](https://user-images.githubusercontent.com/47899873/80351070-5fa11000-887a-11ea-98d3-d0b70edde5d1.png)

Create Template:


![Create_template](https://user-images.githubusercontent.com/47899873/80351177-8e1eeb00-887a-11ea-8c1a-a725cd27f6ce.png)

View Templates:

![view_templates](https://user-images.githubusercontent.com/47899873/80351234-a5f66f00-887a-11ea-8e67-b56fc9b9723a.png)

When you create a group, you become admin of that group.
As admin, You can accept join requests or remove users from your group.
As admin you can also send the emails ( The final purpose of this project )

![send_emails](https://user-images.githubusercontent.com/47899873/80351418-f40b7280-887a-11ea-81cd-769d7cfc5b1e.png)


##### Communication

By default the comunication is made on localhost.
If you want to make this project work online, you can upload the server on an online host.
Before that, you have to change HOST and PORT from both server.py and utils.py to the host IP and the port you want the communication to be made.

Server files:
	server.py
	email_script.py
