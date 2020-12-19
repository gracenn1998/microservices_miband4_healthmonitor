FROM node:lts-alpine

WORKDIR /app

COPY ./vue-app .

EXPOSE 8080

RUN npm install

CMD ["npm", "run", "serve"]

