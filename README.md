# jenkins-fsb

Jenkins instance with preconfigured jobs to analyze Java binaries using Find Security Bugs.


## Usage

Clone the repository

    git clone https://github.com/gosecure/jenkins-fsb && cd jenkins-fsb

Start the tool with `docker-compose`

    docker-compose up -d

Navigate to http://localhost:9457/jenkins

## Changing the default password

Use the htpasswd utility command to override the password.

```
docker-compose exec web /usr/bin/htpasswd -c /etc/nginx/pass/codescan.htpasswd admin
```
