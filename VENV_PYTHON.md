
## virtualenv

### Configuration file

nano ~/.virtualenv/virtualenv.ini

```sh

# create virtual env inside a pwd path
virtualenv env

# use one python version
virtualenv --python=/usr/bin/python3 env

# to activate the virtual env
source env/bin/activate

# to install all dependecies from requeriments file
pip install -r utils/requirements.txt

# to leave virtual env
deactivate

```

## To run using gunicorn use:

```sh
gunicorn -k eventlet -w 1 -b 127.0.0.1:5000 wsgi:ws

# this will start in port: 8000
gunicorn --worker-class eventlet -w 1 wsgi:ws
```