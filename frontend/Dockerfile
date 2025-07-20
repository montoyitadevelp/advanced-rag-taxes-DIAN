# frontend/Dockerfile

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copia solo package.json y lock
COPY package*.json ./

# Asegúrate de que se instalen TODAS las dependencias
ENV NODE_ENV=development
RUN npm install

# Copia todo el código
COPY . .

# Exponer el puerto de desarrollo de Vite
EXPOSE 5173

# Usa el script definido en package.json
CMD ["npm", "run", "dev"]
