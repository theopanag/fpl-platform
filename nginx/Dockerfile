FROM nginx:1.25-alpine

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY sites-available/ /etc/nginx/sites-available/

# Create sites-enabled directory and enable our site
RUN mkdir -p /etc/nginx/sites-enabled && \
    ln -s /etc/nginx/sites-available/fpl-platform.conf /etc/nginx/sites-enabled/

# Create directory for SSL certificates (for future use)
RUN mkdir -p /etc/nginx/ssl

# Create nginx user if it doesn't exist
RUN addgroup -g 101 -S nginx || true
RUN adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx || true

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]