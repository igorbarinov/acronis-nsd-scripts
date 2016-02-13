# Load testing scripts for nrd.ru pilot project

Install dependencies

pip install -r requirements.txt


Files:

load.ini - configuration file, updated by setup_ledger.py

create_voters.py - create pairs of RSA key for voters and save them in pickle files in data/ directory for future usage

locusfile.py - main loading script

setup_ledger.py - create a user and a journal in Acronis Ledger for load tests and store the data in load.ini file for future usage
