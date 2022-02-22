# Welcome to GST Management System

## About

This Project is developed as a part of Interview Process of RedCarpet

[Features Completed So Far](/docs/fetures.md)

[All features](https://pastebin.com/KxYPDsre) in this application are requested by them only.

## Backend-API

[PostMan Collection](https://documenter.getpostman.com/view/13855108/UVkjwdD1)

### Question Answered

#### Q: How will you set the role of a user ?

Since I am maintaining seperate table for each user ,I dont need role field.

#### Q: How you are creating/salting/hashing the passwords?

I am using default hashing system provided by Django as it will be faster for development

#### Q:  Will you use a token? a username/password ?  Are you using JWT?

authenticate user with username/password at login endpoint to generate tokens, request we will use token(JWT) for rest, If token expires .

#### Q: How will you handle roles in an API?

Since I am using sepearate tables for each user-type,default django-authenticator will not work, So I will add 2 new authenticators which can handle different user models

### Other Questions

#### Q: How to Run Django Tests in Docker?

Fixtures will load automatically
In App Folder Run ```python3 manage.py test```
We can run test based on App also

Ex:

```python3 manage.py test gst```

```python3 manage.py test api```

#### Q: Why Changes in Features 5th Point?

Since we are developing GST management system we will take GSTIN and Sales Income from sales of products and services,
GST is not levied on Salary and income from share market those are covered by Direct Tax(Income Tax)
