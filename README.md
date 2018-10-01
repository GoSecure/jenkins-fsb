# jenkins-fsb

Jenkins instance with preconfigured jobs to analyze Java binaries using Find Security Bugs.


## Usage

Clone the repository

    git clone https://github.com/gosecure/codescanner && cd codescanner

Start the tool with `docker-compose`

    docker-compose up -d

Navigate to http://localhost:9457/jenkins

## Changing the default password

1. Obtain the docker container id
```
> docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS
   NAMES
71681c498661        jenkins-fsb_web       "bash -c 'service fc…"   4 minutes ago       Up 4 minutes        0.0.0.0:9457->80/tcp   jenkins-fsb_web_1
```

2. Use the `htpasswd` utility command to override the password.
```
docker exec -it 71681c498661 /usr/bin/htpasswd -c /etc/nginx/pass/codescan.htpasswd admin`
```
