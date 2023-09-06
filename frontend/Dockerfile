# Use the Node.js 14 base image
FROM node:14

# Set the working directory in the Docker image
WORKDIR /app

# Copy the frontend code into the Docker image
COPY . /app

# Install dependencies and build the frontend application
RUN npm install
RUN npm run build

EXPOSE 3000

# Set the entry point command to run a web server
CMD ["npm", "start"]