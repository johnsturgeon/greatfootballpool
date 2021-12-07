# Great Football Pool
## Quick overview of the technology of the new website
This is a Python/Flask website that is for running a friendly 'pick the winner' style football pool.  I find the python language easier to use, and the flask framework is extremely easy to understand and develop with.


# TGFP Readme

Notes: README is divided up into two parts, one for development, and the other for maintenance and depoloyment to production.

# Development

## Prerequisites
* python 3.6 or above
* Discord Server for bots
* Healthchecks.io account
* Sentry.io account
* `sentry-cli` https://docs.sentry.io/product/cli/
* MongoDB
* `jq` https://stedolan.github.io/jq/download/


### Full Stack Development
NOTES:
Full stack development can be deployed by following these steps:

1. Clone this repo
`git clone git@github.com:johnsturgeon/greatfootballpool.git`
2. Run the `bin/setup.py` script
> NOTES:  
> You can review the contents of conf/template.env to determine the variables you will be prompted for  

```bash
cd greatfootballpool
bin/setup_development_full_stack.sh
```
3. test the server
```bash
source env/bin/activate
flask_site/run.sh
```
## Committing and Deploying

Commit with a commit similar to
```bash
resolves issue #4, added 'this weeks results' to the all picks page

```
To auto resolve issues.

Deployment happens on any PR that gets pushed to 'head'

## Discord notes
### Getting your discord auth token
### Setting up your guild
### Setting up a development guild

## Flask notes
see https://flask.palletsprojects.com/en/1.1.x/quickstart/ for generating a good secret key
quick: use: python -c 'import os; print(os.urandom(16))'

# Production

### Production Web Server
> NOTES:   
> Github will deploy to the production web server whenever there is a push to ‘head’ branch.  The configuration for deployment is taken from GitHub secrets.  Deployment can also be done via a script from the ‘bin’ folder (`deploy_web_server.sh`)  
### Production Discord Bot
> NOTES:  
> Github will deploy to the production web server whenever there is a push to ‘head’ branch.  The configuration for deployment is taken from GitHub secrets.  Deployment can also be done via a script from the ‘bin’ folder (`deploy_discord_bot.sh`)  

