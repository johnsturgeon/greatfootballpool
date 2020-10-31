# Great Football Pool
## Quick overview of the technology of the new website
This is a Python/Flask web site that is for running a friendly 'pick the winner' style football pool.  I find the python language easier to use, and the flask framework is extremely easy to understand and develop with.


# TGFP Readme
## Prerequisites (dev and prod)
* python 3.6 or above
* Discord Server for bots
* Healthchecks.io account
* Sentry.io account
* MongoDB
* jq

## Setting up sentry-cli
TODO: I need to add instructions for how to set up sentry-cli here.
## install jq

## Deployment
**There are three types of deployment**
1. Production Web Server
2. Production Discord Bot
3. Full Stack Development (both web server and discord bot configured for production environment)

### Production Web Server
> NOTES:   
> Github will deploy to the production web server whenever there is a push to ‘head’ branch.  The configuration for deployment is taken from GitHub secrets.  Deployment can also be done via a script from the ‘bin’ folder (`deploy_web_server.sh`)  
### Production Discord Bot
> NOTES:  
> Github will deploy to the production web server whenever there is a push to ‘head’ branch.  The configuration for deployment is taken from GitHub secrets.  Deployment can also be done via a script from the ‘bin’ folder (`deploy_discord_bot.sh`)  
### Full Stack Development
NOTES:
Full stack development can be deployed by following these steps:

1. Clone this repo
`git clone git@github.com:johnsturgeon/greatfootballpool.git`
2. Run the setup script
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


