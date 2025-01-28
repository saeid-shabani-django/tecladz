>"in software, the most beautiful code is the one that works." 
>linus torvalds
# Techlads website DRF
---
***what is the project?***
this is a simple website shopping, created as a test for tecladz team<br />

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

Then in the project directory run this command:<br />
`docker-compose up --build`<br />
It will create four containers: One for Django and one for PostgreSql as the database for the project. redis and celery_worker are also included , All the required packages will be installed.

## install a new package

-   Attention: If you want to install a package for django project you should run this command:<br />
`docker-compose exec web pip install <package-name>`<br />
Don't forget to add the new package to requirements.txt for further use:<br />
`docker-compose exec web pip freeze > requirements.txt`



## run the website<br />
after running the docker, insert code below to your terminal:<br />
`docker-compose exec web python manage.py makemigrations`<br />
and then:<br />
`docker-compose exec web python manage.py migrate`<br />
now, you are created the tables, run the project:<br />
`docker-compose up`<br />
insert link below in the browser:<br />
`127.0.0.1:8000`<br />
first of all, you need to registration process:<br />
`http://127.0.0.1:8000/auth/users/`<br />
remember, the registration process is based on EMAIL and PASSWORD. after insert the email and password, check your email address, we have sent an link for verification.<br />
you MUST replace your email and password in settings.py <br />
EMAIL_HOST_USER  =  'your email'<br />
EMAIL_HOST_PASSWORD  =  'your password'<br />
if you use gmail, this [link](https://support.google.com/a/answer/6260879?hl=en) could help you.(you can use console instead for test) <br />
after click on link you will redirect to login page:<br />
``http://127.0.0.1:8000/auth/login/``<br />
or login from here:<br />
`http://127.0.0.1:8000/api-auth/login/`<br />
add products you need,from this url:<br />
`127.0.0.1:8000/products`<br />

# payment process<br />
we are using zarinpal, and sandbox for test, the uuid is generated online you can generate one [here](https://www.uuidgenerator.net/), because you do not need a real uuid (merchant_id)
create a cart id here:<br />
`127.0.0.1:8000/carts/`<br />
add items to your cart here:<br />
`http://127.0.0.1:8000/carts/{cart_id}/items/`<br />
from here you can create your order just insert your cart_id here:<br />
`http://127.0.0.1:8000/orders/`<br />
insert your email and password correct, and you will give a access-token, and refresh-token, save them somewhere.<br />
we recommended to use modheader(for test, if you are using google chrome browser) you can download it as an extension [here](https://modheader.com/)
after installing, enable it, write 'Authorization' as name, and 'JWT your_access_token' as value.<br />
note: JWT must write uppercase, a space is required between JWT and your_access_token
add products you need,from this url:<br />
`127.0.0.1:8000/products`<br />

# payment process<br />
we are using zarinpal, and sandbox for test, the uuid is generated online you can generate one [here](https://www.uuidgenerator.net/), because you do not need a real uuid (merchant_id)
create a cart id here:<br />
`127.0.0.1:8000/carts/`<br />
add items to your cart here:<br />
`http://127.0.0.1:8000/carts/{cart_id}/items/`<br />
from here you can create your order just insert your cart_id here:<br />
`http://127.0.0.1:8000/orders/`<br />
and then go to zarinpal sandbox for payment process:<br />
`http://127.0.0.1:8000/payment/process`<br />
the history of orders are here:<br />
`http://127.0.0.1:8000/orders`<br />

---
notes: <br />
1. you can see list of customers if you are logged in as admid<br />
2. you can add new category if you are admin, and see all categories if not.<br />
3. admin page address is :<br />
`http://127.0.0.1:8000/admin`<br />
and you need, EMAIL and not USERNAME<br />

