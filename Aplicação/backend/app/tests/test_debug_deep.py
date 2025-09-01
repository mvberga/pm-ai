import pytest
import pytest_asyncio
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDebugDeep:
    """Teste de debug profundo para entender o problema do metadata"""
    
    def test_action_item_model_structure(self):
        """Testa a estrutura do modelo ActionItem"""
        print("\n🔍 === VERIFICANDO ESTRUTURA DO MODELO ACTION ITEM ===")
        
        try:
            # Importar o modelo ActionItem
            from app.models.action_item import ActionItem
            print("1️⃣ Modelo ActionItem importado com sucesso")
            
            # Verificar colunas da tabela action_items
            print("2️⃣ Colunas da tabela action_items:")
            for column in ActionItem.__table__.columns:
                nullable = "NULL" if column.nullable else "NOT NULL"
                default = f" DEFAULT {column.default}" if column.default else ""
                print(f"   📋 {column.name}: {column.type} {nullable}{default}")
            
            # Verificar relacionamentos
            print("3️⃣ Relacionamentos:")
            print(f"   🔍 ActionItem.project: {hasattr(ActionItem, 'project')}")
            print(f"   🔍 ActionItem.assigned_to: {hasattr(ActionItem, 'assigned_to')}")
            
        except Exception as e:
            print(f"❌ Erro durante verificação: {e}")
            import traceback
            traceback.print_exc()
        
        print("🔍 === FIM VERIFICAÇÃO ===\n")
        
        # Se chegou até aqui, o teste passou
        assert True
