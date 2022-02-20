# Welcome to GST Management System

## About

This Project is developed as a part of Interview Process of RedCarpet

All features in this appliccation are requested by them only.

### Question Answered

#### Q: How will you set the role of a user ?

Since I am maintaining seperate table for each user ,I dont need role field.

#### Q: How you are creating/salting/hashing the passwords?

I am using default hashing system provided by Django

#### Q:  Will you use a token? a username/password ?  Are you using JWT?

authenticate user with username/password at login endpoint to generate tokens, request we will use token(JWT) for rest, If token expires .

#### Q: How will you handle roles in an API?

Since I am using sepearate tables for each user-type,default django-authenticator will not work, So I will add 2 new authenticators which can handle different user models
