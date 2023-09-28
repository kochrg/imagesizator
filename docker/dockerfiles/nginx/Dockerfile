FROM nginx

COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./sites-available/*.conf /etc/nginx/sites-available/
COPY ./conf/proxy_http.conf /etc/nginx/proxy_http.conf
COPY ./conf/proxy_https.conf /etc/nginx/proxy_https.conf
RUN mkdir -p /srv /srv/imagesizator_service
RUN mkdir -p /srv/imagesizator_service/www /srv/imagesizator_service/logs /srv/imagesizator_service/www/public /srv/imagesizator_service/www/public/static /srv/imagesizator_service/www/public/temp
RUN mkdir -p /srv/imagesizator_service/www/protected /srv/imagesizator_service/www/protected/static /srv/imagesizator_service/www/protected/temp
