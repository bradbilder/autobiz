# Guia de Desenvolvimento Autobiz

## Configuração do Ambiente

### Requisitos

- Python 3.11+
- Node.js 20+
- Docker e Docker Compose
- Git

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/autobiz.git
cd autobiz
```

2. Execute o script de setup:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Ou manualmente:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

## Estrutura de Pastas

```
autobiz/
├── backend/
│   ├── app/
│   │   ├── core/           # Motor auto-modelável
│   │   │   ├── engine.py
│   │   │   ├── schema_generator.py
│   │   │   ├── ui_generator.py
│   │   │   ├── api_generator.py
│   │   │   ├── database_manager.py
│   │   │   └── template_library.py
│   │   ├── models/         # Modelos SQLAlchemy
│   │   │   ├── base.py
│   │   │   ├── tenant.py
│   │   │   └── dynamic.py
│   │   ├── routers/        # Endpoints da API
│   │   │   ├── auth.py
│   │   │   ├── onboarding.py
│   │   │   ├── admin.py
│   │   │   ├── dynamic_crud.py
│   │   │   ├── schema.py
│   │   │   ├── reports.py
│   │   │   ├── integrations.py
│   │   │   ├── plugins.py
│   │   │   └── webhook.py
│   │   ├── services/       # Lógica de negócio
│   │   │   ├── ai_classifier.py
│   │   │   ├── report_generator.py
│   │   │   └── integration_service.py
│   │   ├── plugins/        # Sistema de plugins
│   │   │   ├── base.py
│   │   │   └── manager.py
│   │   └── templates/      # Templates de email
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   └── alembic/            # Migrações
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   │   ├── common/
│   │   │   ├── dashboard/
│   │   │   ├── forms/
│   │   │   └── layout/
│   │   ├── pages/          # Páginas da aplicação
│   │   │   ├── admin/
│   │   │   └── ...
│   │   ├── services/       # Serviços de API
│   │   ├── store/          # Zustand stores
│   │   └── hooks/          # Custom hooks
│   └── public/             # Arquivos estáticos
└── docs/                   # Documentação
```

## Desenvolvimento Backend

### Executando o Servidor

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000

### Documentação da API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Criando um Novo Endpoint

1. Crie um arquivo em `app/routers/`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/exemplo")
async def exemplo():
    return {"message": "Hello World"}
```

2. Registre no `app/main.py`:

```python
from app.routers import exemplo

app.include_router(exemplo.router, prefix="/api/v1/exemplo", tags=["Exemplo"])
```

### Trabalhando com Banco de Dados

#### Criando um Modelo

```python
from sqlalchemy import Column, String, Integer
from app.models.base import BaseModel

class MeuModelo(BaseModel):
    __tablename__ = "meu_modelo"
    
    nome = Column(String(255), nullable=False)
    valor = Column(Integer, default=0)
```

#### Criando uma Migração

```bash
cd backend
alembic revision --autogenerate -m "Descrição da migração"
alembic upgrade head
```

### Testes

```bash
cd backend
pytest
pytest --cov  # Com cobertura
```

## Desenvolvimento Frontend

### Executando o Servidor

```bash
cd frontend
npm run dev
```

A aplicação estará disponível em: http://localhost:5173

### Criando um Componente

```jsx
// src/components/MeuComponente.jsx
import { cn } from '@/utils/helpers'

export default function MeuComponente({ title, children }) {
  return (
    <div className="bg-card border border-border rounded-xl p-6">
      <h2 className="text-xl font-bold mb-4">{title}</h2>
      {children}
    </div>
  )
}
```

### Criando uma Página

```jsx
// src/pages/MinhaPagina.jsx
import { useState, useEffect } from 'react'

export default function MinhaPagina() {
  const [data, setData] = useState(null)

  useEffect(() => {
    // Carregar dados
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Minha Página</h1>
    </div>
  )
}
```

### Adicionando ao Router

```jsx
// src/App.jsx
import MinhaPagina from './pages/MinhaPagina'

<Route path="/minha-pagina" element={<MinhaPagina />} />
```

### Testes

```bash
cd frontend
npm run test
```

## Padrões de Código

### Python

- Siga o PEP 8
- Use type hints
- Documente funções com docstrings
- Nomes em snake_case

```python
def minha_funcao(parametro: str) -> dict:
    """
    Descrição da função.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
    """
    return {"resultado": parametro}
```

### JavaScript/React

- Use ESLint
- Componentes em PascalCase
- Funções em camelCase
- Constants em UPPER_SNAKE_CASE

```jsx
// Componente
export default function MeuComponente() {
  const [estado, setEstado] = useState(null)
  
  const handleClick = () => {
    setEstado('novo valor')
  }
  
  return <button onClick={handleClick}>Clique</button>
}
```

## Git Workflow

### Branches

- `main`: Código em produção
- `develop`: Código em desenvolvimento
- `feature/nome`: Novas funcionalidades
- `bugfix/nome`: Correções de bugs
- `hotfix/nome`: Correções urgentes

### Commits

Use commits semânticos:

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas diversas

```bash
git commit -m "feat: adiciona sistema de notificações"
git commit -m "fix: corrige login com email inválido"
```

### Pull Requests

1. Crie uma branch para sua feature
2. Faça commits regulares
3. Push para o repositório
4. Abra um Pull Request para `develop`
5. Aguarde code review
6. Merge após aprovação

## Debug

### Backend

```python
import logging

logger = logging.getLogger(__name__)

# No código
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Frontend

```javascript
// Console
console.log('Debug:', variavel)
console.table(array)
console.error('Erro:', erro)

// React DevTools
// Use a extensão do navegador
```

## Deploy

### Staging

```bash
git push origin develop
# Deploy automático
```

### Produção

```bash
git checkout main
git merge develop
git push origin main
# Deploy automático
```

### Manual

```bash
./scripts/deploy.sh production
```

## Troubleshooting

### Problemas Comuns

#### Banco de dados não conecta
```bash
# Verifique se o PostgreSQL está rodando
docker-compose ps

# Reinicie o serviço
docker-compose restart postgres
```

#### Migrações falham
```bash
# Resetar migrações
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head
```

#### Node modules corrompidos
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)

## Contato

Em caso de dúvidas, entre em contato com a equipe de desenvolvimento.
