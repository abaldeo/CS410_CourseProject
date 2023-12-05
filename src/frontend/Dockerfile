FROM node:16

ADD ./extension/package.json .

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install --legacy-peer-deps
RUN npm install serve
WORKDIR /app
ADD . /app

EXPOSE 8000
EXPOSE 35729

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
CMD ["start"]
