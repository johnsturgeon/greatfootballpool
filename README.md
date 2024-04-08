# Great Football Pool [DEPRECATED]

## Notes during massive refactor
This was my 'old' football pool, but it has been replaced by a new one, which all repos are gathered up under the org https://github.com/orgs/TheGreatFootballPool/repositories

### Uses the following
- Install docker
- Make directory somewhere on unix machine
- write this docker compose
```yaml
version: '3.8'

services:
  tgfp-web:
    image: johnofcamas/greatfootballpool:latest
    container_name: tgfp-web
    restart: unless-stopped
    command: doppler run --command="gunicorn -b 0.0.0.0:8000 app:app"
    networks:
      my-network:
        aliases:
          - tgfp-web
    environment:
      - DOPPLER_TOKEN=<insert token here>

  nginx:
    image: nginx:latest
    container_name: nginx
    volumes:
      - ./data/certs:/etc/nginx/certs:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    networks:
      - my-network
    depends_on:
      - tgfp-web

networks:
  my-network:

```
- Create nginx.conf file:
```
events { worker_connections 1024; }

http {

    upstream app_servers {    # Create an upstream for the web servers
        server tgfp-web:80;    # the first server
    }

    server {
        listen 80;
        listen [::]:80;

        server_name greatfootballpool.com www.greatfootballpool.com;
        location / {
            proxy_pass http://tgfp-web:8000;
        }
    }
}

```
- Install cloudflares ssl certificates
  - install into `data/certs`
- (see: https://kb.virtubox.net/knowledgebase/cloudflare-ssl-origin-certificates-nginx/)
- open port 80, 443

