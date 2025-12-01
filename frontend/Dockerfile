# Multi-stage build for frontend
FROM node:20-alpine as builder

WORKDIR /app

# Accept API URL as build argument
ARG VITE_API_URL=http://backend:8000
ENV VITE_API_URL=$VITE_API_URL

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code and config files
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/index.html ./
COPY frontend/vite.config.js ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Build the application
RUN npm run build

# Verify dist directory exists and has files
RUN ls -la /app/dist/

# Final stage
FROM nginx:alpine

# Copy built artifacts from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Verify files were copied
RUN ls -la /usr/share/nginx/html/ || echo "Warning: dist directory may be empty"

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
