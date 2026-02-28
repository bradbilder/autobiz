# Makefile do Autobiz

.PHONY: help setup dev build test clean deploy

# Cores
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m

help: ## Mostra esta ajuda
	@echo "$(BLUE)Autobiz - Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

setup: ## Configura o ambiente de desenvolvimento
	@echo "$(BLUE)🔧 Configurando Autobiz...$(NC)"
	chmod +x scripts/setup.sh
	./scripts/setup.sh

dev: ## Inicia ambiente de desenvolvimento
	@echo "$(BLUE)🚀 Iniciando ambiente de desenvolvimento...$(NC)"
	docker-compose up -d

build: ## Constrói as imagens Docker
	@echo "$(BLUE)🔨 Construindo imagens...$(NC)"
	docker-compose build

stop: ## Para todos os serviços
	@echo "$(YELLOW)🛑 Parando serviços...$(NC)"
	docker-compose down

restart: ## Reinicia todos os serviços
	@echo "$(YELLOW)🔄 Reiniciando serviços...$(NC)"
	docker-compose restart

logs: ## Mostra logs dos serviços
	@docker-compose logs -f

logs-backend: ## Mostra logs do backend
	@docker-compose logs -f backend

logs-frontend: ## Mostra logs do frontend
	@docker-compose logs -f frontend

test-backend: ## Executa testes do backend
	@echo "$(BLUE)🧪 Executando testes do backend...$(NC)"
	docker-compose exec backend pytest

test-frontend: ## Executa testes do frontend
	@echo "$(BLUE)🧪 Executando testes do frontend...$(NC)"
	docker-compose exec frontend npm test

migrate: ## Executa migrações do banco
	@echo "$(BLUE)🔄 Executando migrações...$(NC)"
	docker-compose exec backend alembic upgrade head

makemigrations: ## Cria novas migrações
	@echo "$(BLUE)📝 Criando migrações...$(NC)"
	docker-compose exec backend alembic revision --autogenerate -m "$(msg)"

shell-backend: ## Abre shell no container do backend
	@docker-compose exec backend bash

shell-db: ## Abre shell do PostgreSQL
	@docker-compose exec postgres psql -U autobiz -d autobiz

lint-backend: ## Executa linter no backend
	@echo "$(BLUE)🔍 Linting backend...$(NC)"
	docker-compose exec backend flake8 app/

lint-frontend: ## Executa linter no frontend
	@echo "$(BLUE)🔍 Linting frontend...$(NC)"
	docker-compose exec frontend npm run lint

format-backend: ## Formata código do backend
	@echo "$(BLUE)✨ Formatando backend...$(NC)"
	docker-compose exec backend black app/

clean: ## Limpa containers e volumes
	@echo "$(RED)🧹 Limpando ambiente...$(NC)"
	docker-compose down -v
	docker system prune -f

db-backup: ## Faz backup do banco
	@echo "$(BLUE)💾 Fazendo backup...$(NC)"
	@mkdir -p backups
	@docker-compose exec postgres pg_dump -U autobiz autobiz > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore: ## Restaura backup do banco
	@echo "$(BLUE)📥 Restaurando backup...$(NC)"
	@docker-compose exec -T postgres psql -U autobiz -d autobiz < $(file)

dev-backend: ## Inicia apenas o backend localmente
	@echo "$(BLUE)🚀 Iniciando backend...$(NC)"
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload

dev-frontend: ## Inicia apenas o frontend localmente
	@echo "$(BLUE)🚀 Iniciando frontend...$(NC)"
	cd frontend && npm run dev

install-backend: ## Instala dependências do backend
	@echo "$(BLUE)📦 Instalando dependências do backend...$(NC)"
	cd backend && pip install -r requirements.txt

install-frontend: ## Instala dependências do frontend
	@echo "$(BLUE)📦 Instalando dependências do frontend...$(NC)"
	cd frontend && npm install

update: ## Atualiza dependências
	@echo "$(BLUE)🔄 Atualizando dependências...$(NC)"
	cd backend && pip install -r requirements.txt --upgrade
	cd frontend && npm update

deploy: ## Faz deploy para produção
	@echo "$(GREEN)🚀 Fazendo deploy...$(NC)"
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh production

status: ## Mostra status dos serviços
	@docker-compose ps

url: ## Mostra URLs de acesso
	@echo "$(GREEN)📍 URLs de acesso:$(NC)"
	@echo "  Frontend: http://localhost:5173"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"
