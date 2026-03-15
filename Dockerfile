FROM nginx:alpine

COPY src/index.html /usr/share/nginx/html/index.html
COPY docs/profile.jpg /usr/share/nginx/html/profile.jpg

EXPOSE 80
