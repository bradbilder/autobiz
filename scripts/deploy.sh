#!/bin/bash

# Script de deploy do Autobiz

ENVIRONMENT=${1:-production}

echo "🚀 Deploy do Autobiz - Ambiente: $ENVIRONMENT"

# Verificar variáveis de ambiente
if [ ! -f backend/.env ]; then
    echo "❌ Arquivo backend/.env não encontrado"
    exit 1
fi

# Pull da última versão
echo "📥 Atualizando código..."
git pull origin main

# Construir imagens
echo "🔨 Construindo imagens..."
docker-compose build

# Executar migrações
echo "🔄 Executando migrações..."
docker-compose run --rm backend alembic upgrade head

# Reiniciar serviços
echo "🚀 Reiniciando serviços..."
docker-compose -f docker-compose.yml --profile production up -d

# Limpar imagens antigas
echo "🧹 Limpando imagens antigas..."
docker image prune -f

echo ""
echo "✅ Deploy concluído com sucesso!"
