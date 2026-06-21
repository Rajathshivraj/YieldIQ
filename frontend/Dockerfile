FROM node:18-alpine

WORKDIR /app

# Install dependencies first (for caching)
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Set environment variables for development
ENV PORT=3000
ENV WDS_SOCKET_PORT=0

CMD ["npm", "start"]
