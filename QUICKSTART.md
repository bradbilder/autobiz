# 🚀 Quick Start - Autobiz

Guia rápido para colocar o Autobiz para rodar em minutos!

## ⚡ Opção 1: Docker (Recomendado)

### Pré-requisitos
- Docker
- Docker Compose

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/autobiz.git
cd autobiz
```

2. **Configure o ambiente**
```bash
cp backend/.env.example backend/.env
# Edite backend/.env se necessário
```

3. **Inicie os serviços**
```bash
make setup
# ou manualmente:
docker-compose up -d
```

4. **Acesse a aplicação**
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

### Comandos úteis

```bash
make dev          # Inicia ambiente
make stop         # Para serviços
make logs         # Ver logs
make migrate      # Executa migrações
make test-backend # Executa testes
make url          # Mostra URLs
```

## 💻 Opção 2: Desenvolvimento Local

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis
cp .env.example .env
# Edite .env com suas configurações

# Iniciar servidor
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor
npm run dev
```

### Banco de Dados

```bash
# Com Docker
docker run -d \
  --name autobiz-postgres \
  -e POSTGRES_USER=autobiz \
  -e POSTGRES_PASSWORD=autobiz \
  -e POSTGRES_DB=autobiz \
  -p 5432:5432 \
  postgres:15-alpine

# Redis
docker run -d \
  --name autobiz-redis \
  -p 6379:6379 \
  redis:7-alpine
```

## 🎯 Primeiros Passos

### 1. Criar conta de admin

Acesse http://localhost:5173 e clique em "Criar conta"

### 2. Fazer onboarding

Após criar conta, você será direcionado para o onboarding:
1. Escolha o tipo de negócio
2. Preencha informações da empresa
3. Selecione funcionalidades
4. Personalize a aparência
5. Configure integrações

### 3. Acessar dashboard

Após completar o onboarding, você terá acesso ao dashboard personalizado!

### 4. Login como Admin Master (opcional)

```
Email: admin@autobiz.com
Senha: admin123
```

> ⚠️ **Importante**: Altere a senha do admin master em produção!

## 🔧 Configuração Avançada

### Integrações

Edite `backend/.env`:

```env
# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu_token

# Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token

# Email
SMTP_USER=seu_email
SMTP_PASSWORD=sua_senha
```

### Domínio personalizado

Edite `docker-compose.yml`:

```yaml
environment:
  - FRONTEND_URL=https://seu-dominio.com
```

## 🐛 Troubleshooting

### Problema: Banco não conecta
```bash
docker-compose restart postgres
```

### Problema: Migrações falham
```bash
docker-compose exec backend alembic upgrade head
```

### Problema: Portas ocupadas
```bash
# Verifique o que está usando as portas
lsof -i :5173
lsof -i :8000
lsof -i :5432
```

## 📚 Documentação

- [Arquitetura](docs/architecture.md)
- [Guia de Desenvolvimento](docs/development-guide.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment-guide.md)

## 💬 Suporte

Em caso de dúvidas:
1. Consulte a documentação
2. Verifique os logs: `make logs`
3. Abra uma issue no GitHub

---

**Pronto!** Seu sistema Autobiz está rodando! 🎉
