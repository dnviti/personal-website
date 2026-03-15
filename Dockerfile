FROM nginx:alpine

COPY src/index.html /usr/share/nginx/html/index.html
COPY docs/profile.jpg /usr/share/nginx/html/profile.jpg
COPY docs/Daniele_Viti_CV.html /usr/share/nginx/html/cv.html

EXPOSE 80
