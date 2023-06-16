# Elevator - implemented the business logic for a simplified elevator model in Python


Setup

1) create virtual environment and activate it2) install these packages in env
	=> django==3.0.5
	=> djangorestframework==3.11.0
	=> django-background-tasks==1.2.5
3) clone the github repository ( https://github.com/Ashish-3001/Elevator.git )
4) navigate to the elevator_system folder 
5) run ( optional )
	=> python manage.py makemigrations
	=> python manage.py migrate
6) run 
	=> python manage.py runserver

7) open a second terminal/cmd 
( this terminal is for elevators to process the requests in the background )
	=> activate the virtual environment 
	=> navigate to the elevator_system folder 
	=> run: python manage.py process_tasks


Working 

Ones the project is set up we can use multiple API endpoints to controle the elevator, 
for reference I'm using postman to demonstrate the working of the endpoints.

1) Initialise the elevator system to create ‘n’ elevators in the system

url => http://127.0.0.1:8000/api/initialize-elevator-system/
method => POST
Body => { num_elevators: <value> }

2) Fetch all requests for a given elevator

url => http://127.0.0.1:8000/api/fetch-requests-for-elevator/1/
method => GET

3) Fetch the next destination floor for a given elevator

url => http://127.0.0.1:8000/api/next-destination/1
method => GET

4) Fetch if the elevator is moving up or down currently

url => http://127.0.0.1:8000/api/status/1
method => GET

5) Saves user request to the list of requests for a elevator

url => http://127.0.0.1:8000/api/submit-request/
method => POST
Body => { floor: <value> }

6) Mark a elevator as not working or in maintenance 

url => http://127.0.0.1:8000/api/operate_elevator_door/
method => POST
Body => { elevator_number: <value> }

7) Open/close the door.

url => http://127.0.0.1:8000/api/operate_elevator_door/
method => POST
Body => { elevator_number: <value> , action: <"open" or "close"> }

Default Django Rest Framework opens on: http://127.0.0.1:8000/api/

Default Django admin panal opens on: http://127.0.0.1:8000/admin

Basic Frontend opens on: http://127.0.0.1:8000/ 
( still working on the frontend many features needs to added )

Refer this demo vedio for proper understanding and working of the project: 
https://drive.google.com/file/d/11fH-An_63lzs47b1Dg_4kIKb61gw2-IQ/view?usp=sharing



