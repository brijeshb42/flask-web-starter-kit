mkvirtualenv $1
workon $1
pip install -r requirements.txt
npm install
bower install
cp config.py.default config.py
cd frontend
ln -s ../bower_components/ bower_components
