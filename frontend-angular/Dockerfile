# Stage 1: Build
FROM node:20-alpine AS build-step
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build -- --configuration production

# Stage 2: Serve
FROM nginx:alpine
# Αντιγράφουμε τα αρχεία από το build stage στον Nginx
# ΠΡΟΣΟΧΗ: Το path 'dist/frontend-angular/browser' μπορεί να διαφέρει ανάλογα με το όνομα του project σου
COPY --from=build-step /app/dist/frontend-angular/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]