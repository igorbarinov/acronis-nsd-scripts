# Load testing scripts for the nsd.ru pilot project

## Prerequsites

python for scenario execution
nodejs&npm for reports server

## Installation

Clone the repo:

`https://github.com/igorbarinov/acronis-nrd-scripts.git`

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

To see html report with voting results after test scenario:

1. Run report generation script `python publish_results.py`

2. Start expressjs web-server from the reports directory `npm start`

3. Open a web browser `http://127.0.0.1:8080` and see the results.

## Scripts overview

`load.ini` - configuration file, updated by setup_ledger.py

`create_voters.py` - create pairs of RSA key for voters and save them in pickle files in data/ directory for future usage

`locusfile.py` - main load generation script

`setup_ledger.py` - create a user and a journal in Acronis Ledger for load tests and store the data in load.ini file for future usage

`publish_results.py` - generates raw and html reports for voting in directory /reports/public. To see html report start expressjs server in 'reports' directory by command "npm start"
