# BucketList-API

The innovative bucketlist app is an application that allows users  to record and share things they want to achieve or experience before reaching a certain age meeting the needs of keeping track of their dreams and goals. This is the backend API for enabling users to perform crud operations on bucketlists and items with user persistence.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
- Just clone this repository by typing: `https://github.com/Lemmah/BucketList-API.git`
- Switch to project directory: `cd BucketList-API`
- Install project requirements using python pip. But wait, you have to have some stuff before you get to this point. So these are:

### Prerequisites

- Python3.5 and above
- Python virtual environment
Just type:
```
python -V
```
in your terminal and if its not greater than or equal to 3.5, you're not in big trouble, there are tons of tutorials to get up up and running with these. Just grub one then come back when done.

### Installing

Now, you have python3 and a way of running a virtual environment. Lets set up the project environment.(remember we're still in the app directory)

1. Create your virtual environment. Usually, without any wrappers:
```
python -m venv my_venv
```
2. Start your virtual environment:
```
source my_venv/bin/activate
```
3. Install the project requirements specified in the requirements.txt file. Usually,
```
pip install -r requirements.txt
```
4. *Do Migrations*. This application uses postgresql. If you don't have psql you may install it here.
Create a `flask_api` database to be used by the application while running on your localhost.
Then, you can do migrations as:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

This is enough to get you started.
You can now run the application using:

`python runapi.py`


## Running the tests

Easy, just:
`pytest tests/`

## API Endpoints
You can use postman or even curl to reach out to the following api endpoints:

URL Endpoint	|               HTTP Request   | Resource Accessed | Access Type|
----------------|-----------------|-------------|------------------
/api/bucketlists/auth/register   |      POST	| Register a new user|publc
/api/bucketlists/auth/login	  |     POST	| Login and retrieve token|public
/api/bucketlists/auth/logout	  |     POST	| Logout and thus deactivate token|public
/api/bucketlists/auth/reset-password	  |     PUT	| Reset your password when logged in|private
/api/bucketlists	              |      POST	|Create a new Bucketlist|private
/api/bucketlists	              |      GET	|     Retrieve all bucketlists for user|private
/api/bucketlists/<buckelist_id>            |  	GET	    | Retrieve a bucketlist by ID | private
/api/bucketlists/<bucketlist_id>	          |      PUT	|     Update a bucketlist |private
/api/bucketlists/<bucketlist_id>	          |      DELETE	| Delete a bucketlist |private
/api/bucketlists/<bucketlist_id>/items/  |           GET    |Retrive items in a given bucket list|private
/api/bucketlists/<bucketlist_id>/items/     |     POST	| Create items in a bucketlist |private
/api/bucketlists/<bucketlist_id>/items/<item_id>|	DELETE	| Delete an item in a bucketlist |prvate
/api/bucketlists/<bucketlist_id>/items/<item_id>|	PUT   	|update a bucketlist item details |private


## Deployment

This app is ready for Heroku. You can deploy your copy of this app by:
`heroku create <your_url_name>` (where <your_url_name> is what you want to call your app)
`git push heroku master` 
..and boom, you're done! You can chat me on gitter in case of any problems.(gitter link is on badge above)
If you have never worked with Heroku, you can learn how to [Deploy Python Applications on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
## Built With

* [Python Flask](https://www.fullstackpython.com/flask.html) - The web framework used for this API

## Contributing

You can create your pull request. :D

## Versioning

For the versions available, see the [tags on this repository](https://github.com/lemmah/BucketList/tags). 

## Authors

* **James Lemayian** - *Kickstarting the project* - [@Lemmah](https://github.com/lemmah)


## License

This project is currently under the [Creative Commons](https://creativecommons.org/) attribution.

## Acknowledgments

* Andela Kenya - Inspiring the idea.

