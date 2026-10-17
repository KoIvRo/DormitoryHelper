FROM node:20-alpine AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY public ./public
COPY src ./src

RUN npm run build

FROM nginx:1.27-alpine AS runtime

ENV NGINX_ENTRYPOINT_QUIET_LOGS=1

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-main.conf /etc/nginx/nginx.conf
COPY --from=build --chown=nginx:nginx /app/build /usr/share/nginx/html

RUN chown -R nginx:nginx /var/cache/nginx

USER nginx
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
