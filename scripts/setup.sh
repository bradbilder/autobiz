#!/bin/bash

# Script de setup do Autobiz

echo "🚀 Configurando Autobiz..."

# Verificar dependências
command -v docker >/dev/null 2>&1 || { echo "❌ Docker não está instalado. Instale o Docker primeiro."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose não está instalado. Instale o Docker Compose primeiro."; exit 1; }

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p backend/uploads
mkdir -p backend/plugins
mkdir -p database/migrations
mkdir -p database/seeds

# Copiar .env se não existir
if [ ! -f backend/.env ]; then
    echo "⚙️  Criando arquivo .env..."
    cp backend/.env.example backend/.env
    echo "📝 Edite o arquivo backend/.env com suas configurações"
fi

# Construir imagens
echo "🔨 Construindo imagens Docker..."
docker-compose build

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose up -d postgres redis

# Aguardar PostgreSQL
echo "⏳ Aguardando PostgreSQL..."
sleep 5

# Executar migrações
echo "🔄 Executando migrações..."
cd backend
docker-compose exec backend alembic upgrade head || echo "⚠️  Migrações devem ser executadas manualmente"
cd ..

# Iniciar todos os serviços
echo "🚀 Iniciando todos os serviços..."
docker-compose up -d

echo ""
echo "✅ Autobiz configurado com sucesso!"
echo ""
echo "📍 Acesse:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📖 Para mais informações, consulte o README.md"
