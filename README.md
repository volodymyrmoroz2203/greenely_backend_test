<h3>Overview</h3>

<p>In this version of task solution I used Django 4.0.3 as the base of project.</p>
<p>I created models based on provided SQLite DB.</p>
<p>As user auth system Django auth was used and appropriate auth tables where created with migrations.</p>
<p>Filled users table using migration that runs python code (consumption_api/migrations/0001_initial.py).</p>

<p>I wanted to write it using Django, but now I see that the Django REST Framework should be used, because I can't provide HTTP Basic Auth with Django.</p>

<p>Time spent: near 5 hours</p>

<h3>Run project</h3>

1. Install virtualenv: `pip3 install virtualenv`
2. Go to `<directory_with_cloned_project>/greenely_backend_test/`
3. Create venv for project: `virtualenv -p python3 venv`
4. Activate venv: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`
6. Run server: `python manage.py runserver`

<h3>Run tests</h3>

`python manage.py test consumption_api`

<h3>API usage</h3>

At `http://127.0.0.1:8000/` you can log in or log out. 
For login can be used any user with username `user_1` to `user_200`.
Password for all users is `password`.

<h3>Endpoints</h3>

- `/` - home page. Contains link to log in or logout.
- `/accounts/login` - log in form
- `/accounts/logout` - logout
- `/limits` - limits for current user if logged in, redirect to log in page otherwise.
- `/data?start=2014-04-01&count=8&resolution=M` - get data according to params
