# Getting Started

Dependencies

- [serverless](https://www.serverless.com/)
- [jq](https://jqlang.github.io/jq/)

You can install those dependencies the code below

```shell
npm install -g serverless
sudo apt update -y && sudo apt install jq -y
```

# Deploying and testing the project

Inside project folder, once having your aws credentials configured, you can execute commands below to instal and deploy the project, and also execute some tests

### 1. Adjusting bucket name
Remember to change the bucket name, it should be unique.
Change it on [serverless.yml](serverless.yml) and [putEventsPizzaria.py](putEventsPizzaria.py) files

You can achieve that with the command (Just change FIAP_SERVERLESS_PIZZARIA_BUCKET_NAME value to the desired name)

```shell
FIAP_SERVERLESS_PIZZARIA_BUCKET_NAME=some-bucket-name
sed -i "s/pizzaria-edson-reimon-vassa-wendel/${FIAP_SERVERLESS_PIZZARIA_BUCKET_NAME}/g" serverless.yml
sed -i "s/pizzaria-edson-reimon-vassa-wendel/${FIAP_SERVERLESS_PIZZARIA_BUCKET_NAME}/g" putEventsPizzaria.py

```

### 2. Install project dependencies

```shell
pip3 install -r requirements.txt
```

### 3. Deploy to AWS

```shell
sls deploy --verbose --force
```

### 4. Test

First, change 
```shell
python3 putEventsPizzaria.py
```
