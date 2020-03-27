FROM nginx:latest
RUN apt-get update && apt-get install -y net-tools iproute2 iputils-ping curl 
COPY web/index.html /usr/share/nginx/html
COPY web/app.js /usr/share/nginx/html

