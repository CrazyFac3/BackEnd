# How to work with Virtual Environment
When you work on the project you should work with virtual environment. virtual environment enables you to make sure you are using the exact same libraries as the rest
of the team. The 'bin' folder contains the python version and all the libraries used in the project.
## How to use Virtual Environment
If you want for example to run manage.py, make sure you are running it from the venv (virtual environment). 
In order to Run your code from the virtual environment.

In order to set up the venv navigate to the project's folder:
for linux:
`source bin/activate`
for windows:
`%HOMEPATH%\eb-virt\Scripts\activate`


If you want for example to run manage.py on linux:
```
User:~/Projects/GithubProjects/BackEnd$ source bin/activate
(BackEnd) User:~/Projects/GithubProjects/BackEnd$ python manage.py runserver
```
