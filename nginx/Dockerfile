# nginx/Dockerfile
FROM nginx:1.21-alpine

# Remove default configuration and copy our custom one
RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

