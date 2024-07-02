# Use the official Node.js image
FROM node:14

# Create and change to the app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Copy app files
COPY . .

# Generate the report
RUN node generateReport.js

# Expose the port the app runs on
EXPOSE 3000

# Start the server
CMD [ "node", "server.js" ]
