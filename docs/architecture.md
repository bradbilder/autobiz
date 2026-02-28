# Arquitetura do Autobiz

## Visão Geral

O Autobiz é uma plataforma SaaS multi-tenant com arquitetura auto-modelável. O sistema se adapta automaticamente ao tipo de negócio do cliente através de um motor de geração dinâmica.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Web App   │  │  Mobile App │  │  API Externa│             │
│  │   (React)   │  │   (Futuro)  │  │             │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
└─────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │
          └────────────────┴────────────────┘
                           │
                    ┌──────┴──────┐
                    │    Nginx    │
                    │Reverse Proxy│
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
    │  Frontend │   │  Backend  │   │  Static   │
    │  (React)  │   │ (FastAPI) │   │  Files    │
    └───────────┘   └─────┬─────┘   └───────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐
    │ PostgreSQL│  │   Redis   │  │  Plugins  │
    │  (Dados)  │  │  (Cache)  │  │ (Extensões)│
    └───────────┘  └───────────┘  └───────────┘
```

## Componentes Principais

### 1. Motor Auto-Modelável (Core)

O coração do sistema é o motor que gera estruturas personalizadas:

#### SchemaGenerator
- Gera schemas de banco de dados dinâmicos
- Define entidades, campos, relacionamentos e índices
- Suporta 12+ tipos de negócio pré-configurados

#### UIGenerator
- Gera configurações de interface personalizadas
- Define temas, layouts e componentes
- Adapta-se ao perfil do negócio

#### APIGenerator
- Gera endpoints RESTful automaticamente
- Cria operações CRUD para todas as entidades
- Suporta ações customizadas

#### DatabaseManager
- Gerencia bancos multi-tenant
- Cria schemas isolados por tenant
- Executa migrações e backups

### 2. Sistema Multi-Tenant

#### Isolamento de Dados
- Cada tenant tem seu próprio schema no PostgreSQL
- Dados completamente isolados entre tenants
- Busca por tenant_id em todas as queries

#### Configurações por Tenant
- UI configurável
- Features habilitadas/desabilitadas
- Integrações personalizadas
- Webhooks customizados

### 3. Sistema de Plugins

#### Arquitetura de Plugins
- Interface base para todos os plugins
- Carregamento dinâmico
- Hooks para extensão de funcionalidades

#### Plugins Disponíveis
- Relatórios Avançados
- Notificações SMS
- Programa de Fidelidade
- Multi-filial
- Automação

### 4. Integrações

#### WhatsApp Business (Twilio)
- Envio de mensagens
- Templates de mensagens
- Notificações automáticas

#### Mercado Pago
- Criação de preferências
- Processamento de pagamentos
- Webhooks de notificação

#### Google Calendar
- Sincronização de agendamentos
- Criação de eventos
- Notificações

## Fluxo de Dados

### Onboarding

```
1. Usuário responde questionário
        ↓
2. BusinessClassifier analisa
        ↓
3. TemplateLibrary seleciona template
        ↓
4. SchemaGenerator cria schema
        ↓
5. DatabaseManager cria banco
        ↓
6. UIGenerator configura interface
        ↓
7. APIGenerator cria endpoints
        ↓
8. Sistema pronto para uso!
```

### Requisição API

```
1. Cliente faz requisição
        ↓
2. Nginx recebe e roteia
        ↓
3. FastAPI processa
        ↓
4. Middleware de autenticação
        ↓
5. Identificação do tenant
        ↓
6. Execução da lógica
        ↓
7. Acesso ao banco (schema do tenant)
        ↓
8. Resposta ao cliente
```

## Segurança

### Autenticação
- JWT tokens com expiração
- Refresh tokens
- Senhas hasheadas com bcrypt
- 2FA opcional

### Autorização
- RBAC (Role-Based Access Control)
- Permissões por tenant
- Admin master com acesso total

### Proteção de Dados
- Isolamento completo entre tenants
- SQL injection prevention (SQLAlchemy)
- XSS protection (React)
- CSRF tokens

## Escalabilidade

### Horizontal
- Múltiplas instâncias do backend
- Load balancer (Nginx)
- Banco de dados replicado

### Vertical
- Cache com Redis
- Otimização de queries
- Compressão de respostas

## Monitoramento

### Logs
- Logs estruturados com structlog
- Rastreamento de requisições
- Auditoria de ações

### Métricas
- Prometheus metrics
- Endpoint /health
- Dashboard de monitoramento

## Deploy

### Desenvolvimento
```bash
docker-compose up -d
```

### Produção
```bash
docker-compose -f docker-compose.yml --profile production up -d
```

### CI/CD
- GitHub Actions
- Testes automatizados
- Deploy automático

## Tecnologias

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- Pytest

### Frontend
- React 18
- Vite
- Tailwind CSS
- Zustand
- React Query
- Recharts

### Infraestrutura
- Docker
- Docker Compose
- Nginx
- Let's Encrypt (SSL)

## Considerações Futuras

### Melhorias Planejadas
1. Suporte a GraphQL
2. Aplicativo mobile (React Native)
3. Inteligência artificial para análises
4. Marketplace de plugins
5. White-label para revendedores

### Escalabilidade Futura
1. Kubernetes
2. Microserviços
3. Event sourcing
4. CQRS
