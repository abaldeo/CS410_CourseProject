FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
#COPY ./extension/package.json ./

ENV NODE_PATH=/node_modules

# Install dependencies
RUN npm install --legacy-peer-deps

# Install serve
RUN npm install -g serve

RUN npm install serve


# Copy the rest of your app's source code from your host to your image filesystem
# COPY . .
ADD . /app

# Build the app
RUN npm run build

EXPOSE 8000
EXPOSE 35729
EXPOSE 5000

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["start"]
