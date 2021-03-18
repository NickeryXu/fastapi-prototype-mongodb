# fastapi[mongodb]
## Quickstart
Using docker:
```
docker build -t $docker_tag -f Dockerfile .
docker run [OPTIONS] $docker_tag
```
Create "config" file in project root and set environment variables for application, for example:
```
touch config
echo database="mongodb://localhost:27017" >> config
echo secret_key="welcome1" >> config
```
To run the web application in debug use:
```
uvicorn app.app:app --reload
```
## Deployment
Using pm2:
```
pm2 start start.sh --interpreter=bash --name=$project_name
```
Using docker:
```
docker run --name $project_name -p $port:$port --restart=always $docker_tag
```
## Project structure
```
app
├── api                 - web related stuff
│   └── routes          - web routes
├── core                - application configuration, errors, logging
├── crud                - CRUD related stuff
│   └── functions       - packaged functions for CRUD in service
├── db                  - mongodb related stuff
├── dependencies        - dependencies for project
├── models              - pydantic models for this application
│   └── models          - request models, response models and database models
├── utils               - utils for project without service relationship
├── respcode.py         - response code for i18n
└── app.py              - FastAPI application creation and configuration
```
## Related
Nginx.conf
```
user  root;
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    send_timeout 60;
    sendfile        on;
    keepalive_timeout  650;
    server {
        listen       5000;
        server_name  localhost;
        location / {
            root   /opt/tibetan/tibetan-ui/build;
            index  index.html index.htm;
            try_files $uri /index.html;
            client_max_body_size  1024m;
        }
        location /api {
            proxy_set_header  X-Real-IP $remote_addr;
            proxy_pass_request_headers      on;
            proxy_set_header Upgrade $http_upgrade;
            proxy_http_version 1.1;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_pass http://localhost:8000;
            client_max_body_size  1024m;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```