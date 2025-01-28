>"in software, the most beautiful code is the one that works." 
>linus torvalds
# Techlads website DRF
---
***what is the project?***
this is a simple website shopping, created as a test for tecladz team

---
![](https://img.shields.io/badge/django-green)
![](https://img.shields.io/badge/tecladz-drf-red)  ![](https://img.shields.io/badge/docker-postgresql-red) ![](https://img.shields.io/badge/debugtoolbar-optimization-red) ![](https://img.shields.io/badge/api-jwt-red) ![](https://img.shields.io/badge/celery-redis-red)





# how to use?

**If you want to get notified about the future changes Follow my github account.**
`https://github.com/saeid-shabani-django`
Then make sure Docker is running.
## download the project
`git clone https://github.com/saeid-shabani-django/tecladz-1.0`
-   If you are on windows click on the Docker Desktop icon and wait for about a minute.

Then in the project directory run this command:
`docker-compose up --build`
It will create four containers: One for Django and one for PostgreSql as the database for the project. redis and celery_worker are also included , All the required packages will be installed.

## install a new package

-   Attention: If you want to install a package for django project you should run this command:
`docker-compose exec web pip install <package-name>`
Don't forget to add the new package to requirements.txt for further use:
`docker-compose exec web pip freeze > requirements.txt`



## run the website
after running the docker, insert code below to your terminal:
`docker-compose exec web python manage.py makemigrations`
and then:
`docker-compose exec web python manage.py migrate`
now, you are created the tables, run the project:
`docker-compose up`
insert link below in the browser:
`127.0.0.1:8000`
first of all, you need to registration process:
`http://127.0.0.1:8000/auth/users/`
remember, the registration process is based on EMAIL and PASSWORD. after insert the email and password, check your email address, we have sent an link for verification.
you MUST replace your email and password in settings.py 
EMAIL_HOST_USER  =  'your email'
EMAIL_HOST_PASSWORD  =  'your password'
if you use gmail, this [link](https://support.google.com/a/answer/6260879?hl=en) could help you.(you can use console instead for test) 
after click on link you will redirect to login page:
``http://127.0.0.1:8000/auth/login/``
or login from here:
`http://127.0.0.1:8000/api-auth/login/`
add products you need,from this url:
`127.0.0.1:8000/products`

# payment process
we are using zarinpal, and sandbox for test, the uuid is generated online you can generate one [here](https://www.uuidgenerator.net/), because you do not need a real uuid (merchant_id)
create a cart id here:
`127.0.0.1:8000/carts/`
add items to your cart here:
`http://127.0.0.1:8000/carts/{cart_id}/items/`
from here you can create your order just insert your cart_id here:
`http://127.0.0.1:8000/orders/`
insert your email and password correct, and you will give a access-token, and refresh-token, save them somewhere.
we recommended to use modheader(for test, if you are using google chrome browser) you can download it as an extension [here](https://modheader.com/)
after installing, enable it, write 'Authorization' as name, and 'JWT your_access_token' as value.
note: JWT must write uppercase, a space is required between JWT and your_access_token
add products you need,from this url:
`127.0.0.1:8000/products`

# payment process
we are using zarinpal, and sandbox for test, the uuid is generated online you can generate one [here](https://www.uuidgenerator.net/), because you do not need a real uuid (merchant_id)
create a cart id here:
`127.0.0.1:8000/carts/`
add items to your cart here:
`http://127.0.0.1:8000/carts/{cart_id}/items/`
from here you can create your order just insert your cart_id here:
`http://127.0.0.1:8000/orders/`
and then go to zarinpal sandbox for payment process:
`http://127.0.0.1:8000/payment/process`
the history of orders are here:
`http://127.0.0.1:8000/orders`

---
notes: 
1. you can see list of customers if you are logged in as admid
2. you can add new category if you are admin, and see all categories if not.
3. admin page address is :
`http://127.0.0.1:8000/admin`
and you need, EMAIL and not USERNAME

