# Dockerfile do Frontend Autobiz
FROM node:20-alpine

# Diretório de trabalho
WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar código
COPY . .

# Expor porta
EXPOSE 5173

# Comando de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]
