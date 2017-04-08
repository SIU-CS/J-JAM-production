# J-JAM-production
An AI infused personal blogging web app for users to write about their mental health.


## Members

### Team lead
Ayush Kohli
akohli@siu.edu

### QA Manager
Mark Ira Goldberg
markiragoldberg@siu.edu

### Team
James Pelikan
pelikenesis@siu.edu

Jessica Conner-Strunk
JessicaStrunk@siu.edu


# Get started
```bash
sudo apt-get install python-pip python-dev
sudo apt-get install python-virtualenv

#Create python environment
virtualenv djangofy 

#Add the secret variable to .bashrc
export SECRET='key in mhapsite/secret.py'

#Activate it
source djangofy/bin/activate 

pip install -r requirements

python manage.py runserver
```

## Coding style
[Lets stick to pep8](https://www.python.org/dev/peps/pep-0008/)

```bash
#print only
autopep8 script.py
#inplace changes
autopep8 -i script.py
```
