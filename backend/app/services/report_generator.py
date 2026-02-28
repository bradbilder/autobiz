"""
Gerador de relatórios
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
from sqlalchemy import text, func
import structlog

from app.core.database_manager import DatabaseManager

logger = structlog.get_logger()

db_manager = DatabaseManager()


class ReportGenerator:
    """Gera relatórios e dashboards"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.schema_name = f"tenant_{tenant_id.replace('-', '_')}"
    
    async def get_kpis(self, period: str) -> Dict[str, Any]:
        """Retorna KPIs do dashboard"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            # Definir período
            date_range = self._get_date_range(period)
            
            kpis = {}
            
            # Total de vendas
            result = db.execute(text(f"""
                SELECT COUNT(*), COALESCE(SUM(valor_total), 0)
                FROM {self.schema_name}.vendas
                WHERE data_venda >= :start_date
            """), {"start_date": date_range["start"]})
            
            row = result.fetchone()
            kpis["vendas_count"] = row[0]
            kpis["vendas_total"] = float(row[1])
            
            # Ticket médio
            if kpis["vendas_count"] > 0:
                kpis["ticket_medio"] = kpis["vendas_total"] / kpis["vendas_count"]
            else:
                kpis["ticket_medio"] = 0
            
            # Clientes novos
            result = db.execute(text(f"""
                SELECT COUNT(*)
                FROM {self.schema_name}.clientes
                WHERE created_at >= :start_date
            """), {"start_date": date_range["start"]})
            
            kpis["clientes_novos"] = result.scalar()
            
            # Produtos em falta
            result = db.execute(text(f"""
                SELECT COUNT(*)
                FROM {self.schema_name}.produtos
                WHERE estoque_atual <= estoque_minimo
            """))
            
            kpis["produtos_falta"] = result.scalar()
            
            return kpis
            
        finally:
            db.close()
    
    async def get_charts(self, period: str) -> Dict[str, Any]:
        """Retorna dados para gráficos"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            date_range = self._get_date_range(period)
            
            charts = {}
            
            # Vendas por dia
            result = db.execute(text(f"""
                SELECT 
                    DATE(data_venda) as dia,
                    COUNT(*) as quantidade,
                    COALESCE(SUM(valor_total), 0) as total
                FROM {self.schema_name}.vendas
                WHERE data_venda >= :start_date
                GROUP BY DATE(data_venda)
                ORDER BY dia
            """), {"start_date": date_range["start"]})
            
            charts["vendas_por_dia"] = [
                {"date": str(row[0]), "count": row[1], "total": float(row[2])}
                for row in result
            ]
            
            # Produtos mais vendidos
            result = db.execute(text(f"""
                SELECT 
                    p.nome,
                    SUM(iv.quantidade) as quantidade,
                    SUM(iv.valor_total) as total
                FROM {self.schema_name}.itens_venda iv
                JOIN {self.schema_name}.produtos p ON iv.produto_id = p.id
                JOIN {self.schema_name}.vendas v ON iv.venda_id = v.id
                WHERE v.data_venda >= :start_date
                GROUP BY p.nome
                ORDER BY quantidade DESC
                LIMIT 10
            """), {"start_date": date_range["start"]})
            
            charts["produtos_mais_vendidos"] = [
                {"name": row[0], "quantity": float(row[1]), "total": float(row[2])}
                for row in result
            ]
            
            return charts
            
        finally:
            db.close()
    
    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna atividades recentes"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            activities = []
            
            # Vendas recentes
            result = db.execute(text(f"""
                SELECT 
                    v.id,
                    v.data_venda,
                    v.valor_total,
                    c.nome as cliente
                FROM {self.schema_name}.vendas v
                LEFT JOIN {self.schema_name}.clientes c ON v.cliente_id = c.id
                ORDER BY v.data_venda DESC
                LIMIT :limit
            """), {"limit": limit})
            
            for row in result:
                activities.append({
                    "type": "venda",
                    "id": row[0],
                    "date": row[1].isoformat() if row[1] else None,
                    "description": f"Venda de R$ {float(row[2]):.2f}",
                    "client": row[3],
                })
            
            return sorted(activities, key=lambda x: x["date"], reverse=True)[:limit]
            
        finally:
            db.close()
    
    async def get_alerts(self) -> List[Dict[str, Any]]:
        """Retorna alertas do sistema"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            alerts = []
            
            # Estoque baixo
            result = db.execute(text(f"""
                SELECT nome, estoque_atual, estoque_minimo
                FROM {self.schema_name}.produtos
                WHERE estoque_atual <= estoque_minimo
                ORDER BY estoque_atual
                LIMIT 5
            """))
            
            for row in result:
                alerts.append({
                    "type": "warning",
                    "title": "Estoque Baixo",
                    "message": f"{row[0]} está com apenas {row[1]} unidades",
                })
            
            return alerts
            
        finally:
            db.close()
    
    async def vendas_por_periodo(
        self,
        data_inicio: date,
        data_fim: date
    ) -> Dict[str, Any]:
        """Relatório de vendas por período"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            result = db.execute(text(f"""
                SELECT 
                    DATE(data_venda) as dia,
                    COUNT(*) as quantidade,
                    COALESCE(SUM(valor_total), 0) as total,
                    COALESCE(SUM(desconto), 0) as desconto
                FROM {self.schema_name}.vendas
                WHERE DATE(data_venda) BETWEEN :start AND :end
                GROUP BY DATE(data_venda)
                ORDER BY dia
            """), {"start": data_inicio, "end": data_fim})
            
            items = []
            total_geral = 0
            
            for row in result:
                items.append({
                    "date": str(row[0]),
                    "count": row[1],
                    "total": float(row[2]),
                    "discount": float(row[3]),
                })
                total_geral += float(row[2])
            
            return {
                "period": {"start": str(data_inicio), "end": str(data_fim)},
                "items": items,
                "summary": {
                    "total_sales": len(items),
                    "total_value": total_geral,
                }
            }
            
        finally:
            db.close()
    
    async def vendas_por_produto(
        self,
        data_inicio: date,
        data_fim: date,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Relatório de vendas por produto"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            result = db.execute(text(f"""
                SELECT 
                    p.nome,
                    p.codigo,
                    SUM(iv.quantidade) as quantidade,
                    SUM(iv.valor_total) as total,
                    AVG(iv.valor_unitario) as preco_medio
                FROM {self.schema_name}.itens_venda iv
                JOIN {self.schema_name}.produtos p ON iv.produto_id = p.id
                JOIN {self.schema_name}.vendas v ON iv.venda_id = v.id
                WHERE DATE(v.data_venda) BETWEEN :start AND :end
                GROUP BY p.nome, p.codigo
                ORDER BY quantidade DESC
                LIMIT :limit
            """), {"start": data_inicio, "end": data_fim, "limit": limit})
            
            items = []
            for row in result:
                items.append({
                    "name": row[0],
                    "code": row[1],
                    "quantity": float(row[2]),
                    "total": float(row[3]),
                    "avg_price": float(row[4]),
                })
            
            return {
                "period": {"start": str(data_inicio), "end": str(data_fim)},
                "items": items,
            }
            
        finally:
            db.close()
    
    async def fluxo_caixa(
        self,
        data_inicio: date,
        data_fim: date
    ) -> Dict[str, Any]:
        """Relatório de fluxo de caixa"""
        # TODO: Implementar quando tiver tabela de movimentações
        return {
            "period": {"start": str(data_inicio), "end": str(data_fim)},
            "items": [],
        }
    
    async def posicao_estoque(self) -> Dict[str, Any]:
        """Relatório de posição de estoque"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            result = db.execute(text(f"""
                SELECT 
                    p.nome,
                    p.codigo,
                    p.estoque_atual,
                    p.estoque_minimo,
                    p.preco_custo,
                    p.preco_venda,
                    (p.estoque_atual * p.preco_custo) as valor_estoque
                FROM {self.schema_name}.produtos p
                ORDER BY p.nome
            """))
            
            items = []
            valor_total = 0
            
            for row in result:
                items.append({
                    "name": row[0],
                    "code": row[1],
                    "stock": row[2],
                    "min_stock": row[3],
                    "cost_price": float(row[4]),
                    "sale_price": float(row[5]),
                    "stock_value": float(row[6]),
                })
                valor_total += float(row[6])
            
            return {
                "items": items,
                "summary": {
                    "total_products": len(items),
                    "total_stock_value": valor_total,
                }
            }
            
        finally:
            db.close()
    
    async def analise_clientes(self) -> Dict[str, Any]:
        """Análise de clientes"""
        db = db_manager.get_tenant_session(self.tenant_id)
        
        try:
            # Total de clientes
            result = db.execute(text(f"""
                SELECT COUNT(*) FROM {self.schema_name}.clientes
            """))
            total_clientes = result.scalar()
            
            # Clientes com compras
            result = db.execute(text(f"""
                SELECT COUNT(DISTINCT cliente_id) 
                FROM {self.schema_name}.vendas
                WHERE cliente_id IS NOT NULL
            """))
            clientes_compraram = result.scalar()
            
            # Top clientes
            result = db.execute(text(f"""
                SELECT 
                    c.nome,
                    COUNT(v.id) as compras,
                    COALESCE(SUM(v.valor_total), 0) as total
                FROM {self.schema_name}.clientes c
                LEFT JOIN {self.schema_name}.vendas v ON c.id = v.cliente_id
                GROUP BY c.id, c.nome
                ORDER BY total DESC
                LIMIT 10
            """))
            
            top_clientes = []
            for row in result:
                top_clientes.append({
                    "name": row[0],
                    "purchases": row[1],
                    "total": float(row[2]),
                })
            
            return {
                "summary": {
                    "total_customers": total_clientes,
                    "customers_with_purchases": clientes_compraram,
                },
                "top_customers": top_clientes,
            }
            
        finally:
            db.close()
    
    async def custom_report(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório customizado"""
        # TODO: Implementar relatórios customizados
        return {"message": "Relatório customizado", "config": config}
    
    def _get_date_range(self, period: str) -> Dict[str, datetime]:
        """Retorna range de datas baseado no período"""
        now = datetime.now()
        
        if period == "day":
            start = now - timedelta(days=1)
        elif period == "week":
            start = now - timedelta(weeks=1)
        elif period == "month":
            start = now - timedelta(days=30)
        elif period == "year":
            start = now - timedelta(days=365)
        else:
            start = now - timedelta(days=30)
        
        return {"start": start, "end": now}
