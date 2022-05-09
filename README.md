# Foauth
#### Oauth2 provider with facial verification

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Need to do](#needtodo)

## General info
This project is OAuth provider with facial verification for an authentication process
	
## Technologies
Project is created with:
* python: 3.6
* Tensorflow: 2.0.0
* Flask
* React
* Antd
* PostgreSQL
* Redis

## Setup
To run this project, you need to create virtual env with Anaconda from yml file
```
conda env create -f environment.yml
```
Add env variable
```
$ export AUTHLIB_INSECURE_TRANSPORT=1
```
Run flask
```flask run```
Install npm env and run react server
```
npm install
npm start
```

## Need to do
1. ~~Add Oauth login type in security logs~~
2. ~~Add deletion of clients~~
3. ~~Add revoking of grant access to account~~
4. ~~Add webcam set in Oauth page~~
5. ~~Add photos on front in secutiry logs~~
6. Build react and add it as tempalate in / path
7. ~~Add PostgreSQL integration~~
8. ~~Add Redis for session management ?~~
9. ~~Add API for user info for clients~~
10. ~~Add exception catch when no face in input image~~