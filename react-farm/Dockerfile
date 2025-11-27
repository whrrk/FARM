# 1. build stage
FROM node:22-alpine AS build

WORKDIR /app

# 2. dependencies stage
COPY package.json package-lock.json* ./
RUN npm ci

# 3. copy source code
COPY . .

# 4. vite env variable setting
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 5. build
RUN npm run build

# 5.2 nginx stage
FROM nginx:alpine

# vite built files copy to nginx html directory
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
