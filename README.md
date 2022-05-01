# Jobsin

## _ A complete API for job portal _

This project is done as an example of my work with Python programming language and Django framework.
<img src="https://miro.medium.com/max/700/1*kR89JbQQK9aAkNVyxE63pg.png" width="400" height="250" />
> Django REST framework is an open source, flexible and fully-featured library  with modular and customizable architecture that aims at building sophisticated  web APIs and uses Python and Django.

## Service reference

[Documentation in Persian](https://github.com/boshra-irnd/jobsin/blob/master/README.fa.md)  <img src="https://cdn.countryflags.com/thumbs/iran/flag-round-250.png" width="15" height="15" />




## Employer

Employer can register using username and password.

- Post job opportunities
- See job seekers' requests and job seeker information
- Change their request to one of four options Pending, Rejected, Interview and Hire.

## Jobseeker

Jobseeker can register using username and password.

- See details of work
- See information about organization
- Submit a job application

## Tech

This API uses a number of open source projects to work properly:
- Python 3.8.10 
- DjangoRestFramework 3.13.1
- DjangoRestFramework-Simplejwt 5.1.0

## Setup

Following are the setup instruction for ubuntu 20.04.


install
- git 
- postgresql 
- python3
- python3-dev 
- python3-venv


Then setup env using the following command

```
python3 -m venv my_env
```
Activate env with the following command
```
source my_env/bin/activate
```
Install requirements
```
pip install -r requirements.txt
```
And you have to create a file called dev.py in jobsen/settings and define SECRET_KEY and DATABASES in it.
