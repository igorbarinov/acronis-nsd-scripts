# Load testing scripts for the nrd.ru pilot project

## Scripts description
Install dependencies

`pip install -r requirements.txt`

## How to run load tests?

In a terminal run:

`locust --host=http://167.114.247.67:8080`

Open 

## Scripts overview

`load.ini` - configuration file, updated by setup_ledger.py

`create_voters.py` - create pairs of RSA key for voters and save them in pickle files in data/ directory for future usage

`locusfile.py` - main load generation script

`setup_ledger.py` - create a user and a journal in Acronis Ledger for load tests and store the data in load.ini file for future usage



