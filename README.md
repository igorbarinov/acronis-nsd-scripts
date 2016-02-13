# Load testing scripts for the nrd.ru pilot project

## Scripts description
Install dependencies

`pip install -r requirements.txt`

## How to run load tests?


### Basic scenario

Create user and required data structures in Acronis Ledger:

`python setup_ledger.py`

In a terminal run:

`locust --host=http://167.114.247.67:8080`

Open a web monitor `http://127.0.0.1:8089` and run load test.

![Load](https://api.monosnap.com/rpc/file/download?id=ZpyRHYKB7ZEdxY1bGHUfK18D2b7zhg)


### Advanced scenario

  TODO

## Scripts overview

`load.ini` - configuration file, updated by setup_ledger.py

`create_voters.py` - create pairs of RSA key for voters and save them in pickle files in data/ directory for future usage

`locusfile.py` - main load generation script

`setup_ledger.py` - create a user and a journal in Acronis Ledger for load tests and store the data in load.ini file for future usage



