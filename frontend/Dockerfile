FROM node:20-alpine AS dev

WORKDIR /app

COPY package.json /app/package.json
COPY tsconfig.json /app/tsconfig.json
COPY tsconfig.node.json /app/tsconfig.node.json
COPY vite.config.ts /app/vite.config.ts
COPY index.html /app/index.html
COPY public /app/public
COPY src /app/src

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
