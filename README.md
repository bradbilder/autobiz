# Autobiz - Sistema Auto-Modelável para Gestão de Negócios

Autobiz é uma plataforma SaaS que se adapta automaticamente ao tipo de negócio do cliente. Através de um fluxo de onboarding inteligente, o sistema gera uma estrutura personalizada com banco de dados, APIs e interface de usuário específicos para cada tipo de negócio.

## 🚀 Funcionalidades

### Core
- **Onboarding Inteligente**: Questionário que identifica o tipo de negócio e gera sistema personalizado
- **Banco de Dados Dinâmico**: Schema auto-gerado baseado no perfil do negócio
- **APIs RESTful**: Endpoints auto-gerados para todas as entidades
- **Multi-Tenant**: Isolamento completo de dados entre clientes

### Tipos de Negócio Suportados
- Varejo/Lojas físicas
- E-commerce
- Prestação de Serviços
- Consultoria
- Restaurantes/Delivery
- Clínicas Médicas
- Imobiliárias
- Construção Civil
- Escolas/Instituições
- Academias
- Salões de Beleza
- Oficinas Mecânicas

### Integrações
- **WhatsApp Business**: Comunicação direta com clientes
- **Mercado Pago**: Pagamentos online
- **Google Calendar**: Sincronização de agendamentos
- **Email Marketing**: Campanhas de email

### Sistema de Plugins
- Extensões para funcionalidades adicionais
- API de plugins para desenvolvedores
- Marketplace de plugins

### Painel Admin Master
- Gestão de todos os tenants
- Estatísticas da plataforma
- Gestão de usuários
- Configurações globais

## 🛠️ Tecnologias

### Backend
- **Python 3.11**
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **PostgreSQL**: Banco de dados principal
- **Redis**: Cache e filas
- **Alembic**: Migrações de banco de dados
- **JWT**: Autenticação segura

### Frontend
- **React 18**
- **Vite**: Build tool ultrarrápido
- **Tailwind CSS**: Framework CSS utilitário
- **Zustand**: Gerenciamento de estado
- **React Query**: Gerenciamento de dados
- **Recharts**: Gráficos e visualizações
- **shadcn/ui**: Componentes UI

### Infraestrutura
- **Docker**: Containerização
- **Docker Compose**: Orquestração local
- **Nginx**: Reverse proxy

## 📦 Instalação

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+ (para desenvolvimento frontend)
- Python 3.11+ (para desenvolvimento backend)

### Quick Start com Docker

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/autobiz.git
cd autobiz
```

2. Configure as variáveis de ambiente:
```bash
cp backend/.env.example backend/.env
# Edite o arquivo .env com suas configurações
```

3. Inicie os serviços:
```bash
docker-compose up -d
```

4. Acesse a aplicação:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentação API: http://localhost:8000/docs

### Desenvolvimento Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📁 Estrutura do Projeto

```
autobiz/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── core/           # Motor auto-modelável
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── routers/        # Endpoints da API
│   │   ├── services/       # Lógica de negócio
│   │   ├── plugins/        # Sistema de plugins
│   │   └── templates/      # Templates de email
│   ├── alembic/            # Migrações de banco
│   └── tests/              # Testes
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── services/       # Serviços de API
│   │   ├── store/          # Zustand stores
│   │   └── hooks/          # Custom hooks
│   └── public/             # Arquivos estáticos
├── nginx/                  # Configuração Nginx
├── docs/                   # Documentação
└── scripts/                # Scripts utilitários
```

## 🔧 Configuração

### Variáveis de Ambiente

#### Backend (.env)
```env
# App
DEBUG=true
SECRET_KEY=your-secret-key
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/autobiz
REDIS_URL=redis://localhost:6379/0

# Integrations
OPENAI_API_KEY=sk-...
MERCADOPAGO_ACCESS_TOKEN=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
SMTP_USER=...
SMTP_PASSWORD=...

# Admin
ADMIN_MASTER_EMAIL=admin@autobiz.com
ADMIN_MASTER_PASSWORD=admin123
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🧪 Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 📚 Documentação da API

A documentação completa da API está disponível em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 Deploy

### Produção com Docker Compose

1. Configure as variáveis de ambiente para produção
2. Execute:
```bash
docker-compose -f docker-compose.yml --profile production up -d
```

### Deploy em Cloud

O sistema está preparado para deploy em:
- AWS (ECS, EKS, EC2)
- Google Cloud Platform
- Azure
- Digital Ocean
- Heroku

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Autobiz Team** - *Initial work*

## 🙏 Agradecimentos

- FastAPI pela excelente framework
- React pela biblioteca frontend
- Comunidade open source

---

<p align="center">
  Feito com ❤️ pela equipe Autobiz
</p>
