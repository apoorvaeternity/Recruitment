Instruction to set up the projects

clone the project to your directory

* set up virtual environment for python3

virtualenv venv --no-site-packages

* install the corresponding dependencies from requirement.txt

pip install -r requirement.txt

Here we are using postgresql at backend so i expect that you have postgresql install or else just change the setting.py to your desired database you wanna use. 

* Add the environment variable to the activate.sh script present at venv/bin/activate.These enviroment variable will be use by python to connect with the database

* Create Super User for admin

python manage.py createsuperuser
	
*Run migrations and migrate

python manage.py makemigrations
python manage.py migrate



