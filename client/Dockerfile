FROM node:23-alpine AS builder

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

ARG VITE_API_URL=${VITE_API_URL}

RUN npm run build

FROM nginx:1.25-alpine AS runtime

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]