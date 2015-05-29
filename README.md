# Flask Starter Kit

### Comes with preconfigured basic Flask app with SQLAlchmemy, LoginForm, Basic User Model, and static assets.

### Requirements:
* Python 2.7.x
* `node` with global installation of `gulp` and `bower`. Can be used without that global installations also.

### How to use ?
* Clone this repo `git clone git@github.com:brijeshb42/flask-web-starter-kit.git`.
* Create a new virtual environment `mkvirtualenv starter-kit`.
* Switch to the new env `workon starter-kit`.
* Install python modules `pip install -r requirements.txt`.
* Install node modules to compile assets `npm install`.
* Install bower packages `bower install`.
* Copy `config.py.default` to `config.py`.
* Make changes to `config.py` as required.
* Create a symlink to `bower_components` folder inside `frontend` : `cd frontend && ln -s ../bower_components/ bower_components`.
* Migrate DB (uses sqlite by default. Can be configured in `config.py`)
    * `python script.py db init`
    * `python script.py db migrate`
    * `python script.py db upgrade`
* In separate terminal, `cd` into the `starter-kit` directory and run `gulp clean && gulp` to compile static assets and start a livereload server.
* Then run `python script.py runserver`
* Open `localhost:5000` in browser.
