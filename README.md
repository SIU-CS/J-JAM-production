# J-JAM-production
An AI infused personal blogging web app for users to write about their mental health.

[![Build Status](https://travis-ci.org/SIU-CS/J-JAM-production.svg?branch=master)](https://travis-ci.org/SIU-CS/J-JAM-production)

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
Use branch `master`

```bash
sudo apt-get install python-pip python-dev
sudo apt-get install python-virtualenv

#Create python environment
git clone https://github.com/SIU-CS/J-JAM-production.git
cd J-JAM-production
virtualenv djangofy 

#Make sure all the required api keys are in the .bashrc

#Activate it
source djangofy/bin/activate 

pip install -r requirements

python mhapsite/manage.py makemigrations
python mhapsite/manage.py migrate
python mhapsite/manage.py loaddata ./fixtures/quotes.json
python mhapsite/manage.py runserver


```

## Coding style
[Lets stick to pep8](https://www.python.org/dev/peps/pep-0008/)

```bash
#print only
autopep8 script.py
#inplace changes
autopep8 -i script.py
```
