# Getting started (development)

First time:

Install python in your computer (3.9.6)

Create your aws credentials file on C:\Users\USER_NAME\.aws\credentials

* For more details please follow the next instructions: https://sst.dev/chapters/configure-the-aws-cli.html

In the terminal (cmd for windows) open the path of the project

Run the next commands

## First time:
```bash
pip install pipenv
```

```bash
npm install
```

Personal environment setup
## Personal environment setup
```bash
# install dependencies
cd services/
pipenv shell
pipenv install
cd ..

# run npm in root
npm install 

# create aws personal environment
npx sst start

# if there are issues with the previous command, make sure to have installed this npm packages.
  "@serverless-stack/cli": "^1.18.4",
  "aws-sdk": "^2.1251.0",
  "esbuild": "^0.14.54"
```

## Version SST Update
If you need to update the SST version in your local system, you should follow these steps:

1. Remove your local node_modules directory.
2. Run npm install.
3. For local development, run npx sst dev instead of npx sst start.

IMPORTANT: Don't remove the requirements.txt file as it is required since v2.


## To run linting and unit tests:
```bash
cd services
pipenv shell
pylint functions
pytest --cov-config=.coveragerc --cov=functions --cov-report=html tests/domain/
pytest --cov-config=.coveragerc --cov=functions --cov-report=html tests/api/
```

## How to test an enpoint?
 1. Go to `BackendStack.ts` and check the endpoint you want to test.
 2. `../functions/handlers/auth.login` Inside file **auth** calling **login** function.
 3. Follow the **sst** UI client url generated in the console. And also the one from the aws lambda configuration that appears bellow. 
 

## Deployment
Download docker: 
- Windows: 
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64
- MacOS (Intel chip):
https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module
- MacOS (Apple chip):
https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module
- Linux (Follow this instructions):
https://docs.docker.com/desktop/install/linux-install/

STOP HERE (ONLY WINDOWS USERS)!

If Docker allows you to use WSL 2 instead Hyper-V (recommended by them) please unmark it.

If you use WSL 2 you can follow the next steps BEFORE INSTALLING Docker, but I recommend to use Hyper-V

Before to install docker on windows ONLY IF YOU CHOOSEN WSL 2:

- Open a powershell terminal
- run wsl --install -d UBUNTU-20.04

When the installer from ubuntu opens a new cmd interface:

- insert a username e.g. rrodarte (use a different)
- insert a password (you know what to do)

Install Docker

Open Docker desktop
```bash
# before to do a merge to develop use this stage to test your endpoints 
# (please notify via slack to the entire python team the use of this stage)
npx sst deploy --stage dev-team-python-1

# development env
npx sst deploy --stage dev

# staging env
npx sst deploy --stage staging

# prod env
npx sst deploy --stage prod
```



# References

## List of functions from legacy API
 - https://maxims.atlassian.net/wiki/spaces/H2/pages/106135553/Legacy+API#Raw-exported-function-list

## Environment variables
  * DOMAIN_API
  Type: `String | undefined`
  Example: `my-api-stage.example.com`
  If specified, the AWS account must have a hosted zone for `example.com`, and the script will create a certificate and associate the subdomain
  * LEGACY_FRONT_OFFICE1
  Type: `String | undefined`
  Example: `my_url_to_api_soap_v1`
  * LEGACY_FRONT_OFFICE2
  Type: `String | undefined`
  Example: `my_url_to_api_soap_v2`
  * BASE_API_URL
  Type: `String | undefined`
  Example: `my_url_to_api_hermes_local`
  * ES_CITIES_URI
  Type: `String | undefined`
  Example: `my_url_to_api_hermes_es`
  * USER_ES_CITIES
  Type: `String | undefined`
  Example: `my_user_for_es`
  * PASSWORD_ES_CITIES
  Type: `String | undefined`
  Example: `my_password_for_es`
  * REPORTING_SERVICES_USER
  Type: `String | undefined`
  Example: `my_user_reporting_services`
  * REPORTING_SERVICES_PASSWORD
  Type: `String | undefined`
  Example: `my_password_reporting_services`
  * REPORTING_SERVICES_WSDL
  Type: `String | undefined`
  Example: `my_wsdl_reporting_services`
  * REPORTING_SERVICES_QR_URL
  Type: `String | undefined`
  Example: `my_qr_url_reporting_services`
  * ACCESS_CONTROL_ALLOW_ORIGIN
  Type: `String | undefined`
  Example: `domain_allowed_to_make_requests`
  * BASE_API_REST_KEYCLOAK
  Type: `String | undefined`
  Example: `http://localhost:8080`
  * REALM_KEYCLOAK
  Type: `String | undefined`
  Example: `hermes20`
  * TEST_AUTH_USER
  Type: `String | undefined`
  Example: `test`
  * TEST_AUTH_PASSWORD
  Type: `String | undefined`
  Example: `test`
  * INSIGHTS_ENABLED
  Type: `String | undefined`
  Example: `True`
  * FILE_STORAGE_USER
  Type: `String | undefined`
  Example: `my_user`
  * FILE_STORAGE_PASSWORD
  Type: `String | undefined`
  Example: `my_password`
  * ERP_SERVICES_WSDL
  Type: `String | undefined`
  Example: `https://erp`
  * FILE_STORAGE_URL
  Type: `String | undefined`
  Example: `https://file-storage.com`

  use only if its necessary to don't update your session guid in dynamo table

  * DOMAIN_API
  Type: `String | undefined`  
  Example: `my-api-stage.example.com`
  If specified, the AWS account must have a hosted zone for `example.com`, and the script will create a certificate and associate the subdomain
  * SSM_FRONT_OFFICE_V2
  Type: `String | undefined`
  Example: `my_url_to_api_soap_v2`
  * BASE_API_URL
  Type: `String | undefined`
  Example: `my_url_to_api_hermes_local`
  * BASE_API_REST_KEYCLOAK  
    Type: `String`  
    Keycloak REST url
  * CACHE_TIME  
    Type: `number`  
    Duration of authorizer cache
  * REALM_KEYCLOAK  
    Type: `string`  
    The name of the realm using in keycloak
  * RETENTION_POLICY_LOGS  
    Type: `string`  
    The number of days used to delete logs from cloudwatch
  * AWS_REGION  
    Type: `string`  
    The region that you are using in AWS
  * LOG_RETENTION_DAYS  
    Type: `NUMBER`  
    Number of days that logs will persist before being deleted 


# References
## Libraries
  * Zeep (SOAP Client): https://docs.python-zeep.org/en/master/api.html

This library makes the translation between the SOAP API to REST. In `legacy.py` you
will notice that zeep is used to initialize the client with the SOAP specification URL. You have to add this url to a `.env` file. This is specified in Confluence Legacy API.

## Development
  * Pipenv: https://realpython.com/pipenv-guide/
  * Mocks for unit testing: https://realpython.com/python-mock-library/
  * SST python debugging: https:/sst/www.linen.dev/s/serverless-stack/t/445893/Hey-U01J5Q8HV5Z-U01JVDKASAC-I-ve-successfully-followed-the-G
  * pytest coverage configuration: https://coverage.readthedocs.io/en/latest/config.html
  * python 3.9.6 (windows installer): https://www.python.org/downloads/release/python-396/
  * Secrets manager using SDK for python: https://docs.aws.amazon.com/code-library/latest/ug/python_3_secrets-manager_code_examples.html#w2683aac13c23b7c81c11
  * Read files from python: #https://stackoverflow.com/questions/44426569/python-open-requires-full-path
