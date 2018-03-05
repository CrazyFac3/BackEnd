# CrazyFac3 BackEnd 🤪
The CrazyFac3 BackEnd team is responsible for developing all the server-side in CrazyFac3 app. The server side is
implemented using django framework and hosted by AWS Elastic Beanstalk service.
## How to work with Virtual Environment
Let's say you are working on the project and... Oops! You don't know which packages you need in order to run the project.
That is exactly why we use virtual environment. 
Virtual environment enables you to make sure you are using the exact same libraries as the rest
of the team. The 'bin' and 'Scripts' folders contain the python interpreter and all the libraries used in the project.
### How to use Virtual Environment
Let's say you are now working on the project and you want to run a file. Virtualenv makes sure you are running the file with all
the needed libraries to make it work as expected.

In order to use the virtualenv you will have to **activate** every time you are working on the cmd/terminal
activation for linux:
`source bin/activate`


activation for windows:
`Scripts\activate.bat`


If you want for example to run manage.py on **Unix**:
```
User:~/Projects/BackEnd$ source bin/activate
(BackEnd) User:~/Projects/BackEnd$ python manage.py runserver
```


If you want for example to run manage.py on **Windows**:
```
C:\Users\user\Projects\BackEnd>Scripts\activate
(BackEnd) C:\Users\user\Projects\BackEnd>python manage.py runserver 
```

As you can see, in both unix and windows, after activated venv there will be brackets with the name
of the folder in which you are in. that tells you that you are currently working from the venv on this folder.

## macOS Instructions
To run the django server you'll need an sql support on your machine.
To do so, you should install [Homebrew](https://brew.sh).

After installing Homebrew, you should install `mysql`:
```
brew update
brew install mysql
```

Then, follow the instructions to use the virtual environment.
