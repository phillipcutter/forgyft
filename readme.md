When launching the Docker container, supply these environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- MAILGUN_API_KEY

Optional environment variables can be passed too:
- DJANGO_DEBUG : "1"

Example docker run command:
`docker run -p 80:80 mrfleap/esprza`

Example docker build command:
`docker build -t mrfleap/esprza .`



Deploy steps:
1. Build new Docker image
2. Push new Docker image to hub
3. Pull new Docker image on server
4. Rerun `docker-compose up` on server to refresh web container