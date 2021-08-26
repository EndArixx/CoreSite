# Table Top RPG Stat Website
This is the Example folder. Both the setting.py file and the Database are ignored so copy from here to the following locations to get started:

~\CoreSite\Core\CoreCityStats.sqlite3
~\CoreSite\Core\Core\settings.py




Python3 manage.py runserver ForestRPG.com:80 

to background:

	Screen
	[START SERVER]
	python3 manage.py runserver 162.249.2.141:80

	ctrl + A
	Ctrl + D

to bring it back

	screen -r

for static files
       python3 manage.py collectstatic


apache: 
## Start command ##
systemctl start apache2.service
## Stop command ##
systemctl stop apache2.service
## Restart command ##
systemctl restart apache2.service

service apache2 restart

admin account:
John
WarCrimes1945

migration stuff:
python manage.py makemigrations
python manage.py migrate