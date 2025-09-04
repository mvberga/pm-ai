"""
Testes de integração avançados para endpoints de segurança.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User


class TestSecurityAdvanced:
    """Testes de integração avançados para segurança."""
    
    async def test_security_health_check(self, client: TestClient, db_session: AsyncSession):
        """Testar verificação de saúde da segurança."""
        
        # Testar health check de segurança
        response = client.get(f"{settings.API_V1_STR}/security/health")
        assert response.status_code == 200
        
        health_data = response.json()
        
        # Verificar se todas as métricas estão presentes
        assert "status" in health_data
        assert "timestamp" in health_data
        assert "security_events" in health_data
        assert "threat_level" in health_data
        assert "last_scan" in health_data
        
        # Verificar se o status é válido
        assert health_data["status"] in ["healthy", "warning", "critical"]
        
        # Verificar se o nível de ameaça é válido
        assert health_data["threat_level"] in ["low", "medium", "high", "critical"]
    
    async def test_security_events_listing(self, client: TestClient, db_session: AsyncSession):
        """Testar listagem de eventos de segurança."""
        
        # Testar listagem de eventos de segurança
        response = client.get(f"{settings.API_V1_STR}/security/events")
        assert response.status_code == 200
        
        events_data = response.json()
        
        # Verificar se é uma lista
        assert isinstance(events_data, list)
        
        # Se houver eventos, verificar estrutura
        if events_data:
            event = events_data[0]
            assert "id" in event
            assert "timestamp" in event
            assert "severity" in event
            assert "threat_type" in event
            assert "description" in event
            assert "source_ip" in event
            assert "user_id" in event
    
    async def test_security_events_with_filters(self, client: TestClient, db_session: AsyncSession):
        """Testar listagem de eventos de segurança com filtros."""
        
        # Testar filtro por severidade
        response = client.get(f"{settings.API_V1_STR}/security/events?severity=high")
        assert response.status_code == 200
        
        high_severity_events = response.json()
        assert isinstance(high_severity_events, list)
        
        # Testar filtro por tipo de ameaça
        response = client.get(f"{settings.API_V1_STR}/security/events?threat_type=brute_force")
        assert response.status_code == 200
        
        brute_force_events = response.json()
        assert isinstance(brute_force_events, list)
        
        # Testar filtro por horas
        response = client.get(f"{settings.API_V1_STR}/security/events?hours=24")
        assert response.status_code == 200
        
        recent_events = response.json()
        assert isinstance(recent_events, list)
        
        # Testar filtro por limite
        response = client.get(f"{settings.API_V1_STR}/security/events?limit=10")
        assert response.status_code == 200
        
        limited_events = response.json()
        assert isinstance(limited_events, list)
        assert len(limited_events) <= 10
    
    async def test_security_events_analytics(self, client: TestClient, db_session: AsyncSession):
        """Testar analytics de eventos de segurança."""
        
        # Testar analytics de eventos de segurança
        response = client.get(f"{settings.API_V1_STR}/security/events/analytics")
        assert response.status_code == 200
        
        analytics_data = response.json()
        
        # Verificar se todas as métricas estão presentes
        assert "total_events" in analytics_data
        assert "events_by_severity" in analytics_data
        assert "events_by_type" in analytics_data
        assert "events_by_hour" in analytics_data
        assert "top_threats" in analytics_data
        assert "trend_analysis" in analytics_data
        
        # Verificar estrutura dos dados de severidade
        severity_data = analytics_data["events_by_severity"]
        assert "critical" in severity_data
        assert "high" in severity_data
        assert "medium" in severity_data
        assert "low" in severity_data
        
        # Verificar estrutura dos dados de tipo
        type_data = analytics_data["events_by_type"]
        assert isinstance(type_data, dict)
        
        # Verificar estrutura da análise de tendência
        trend_data = analytics_data["trend_analysis"]
        assert "direction" in trend_data
        assert "change_percentage" in trend_data
        assert "period" in trend_data
    
    async def test_security_threat_detection(self, client: TestClient, db_session: AsyncSession):
        """Testar detecção de ameaças de segurança."""
        
        # Testar detecção de ameaças
        response = client.get(f"{settings.API_V1_STR}/security/threats")
        assert response.status_code == 200
        
        threats_data = response.json()
        
        # Verificar se é uma lista
        assert isinstance(threats_data, list)
        
        # Se houver ameaças, verificar estrutura
        if threats_data:
            threat = threats_data[0]
            assert "id" in threat
            assert "threat_type" in threat
            assert "severity" in threat
            assert "description" in threat
            assert "detected_at" in threat
            assert "status" in threat
            assert "mitigation_status" in threat
    
    async def test_security_threat_mitigation(self, client: TestClient, db_session: AsyncSession):
        """Testar mitigação de ameaças de segurança."""
        
        # Primeiro, obter uma ameaça existente
        response = client.get(f"{settings.API_V1_STR}/security/threats")
        assert response.status_code == 200
        
        threats = response.json()
        
        if threats:
            threat_id = threats[0]["id"]
            
            # Testar mitigação de ameaça
            mitigation_data = {
                "action": "block_ip",
                "description": "Bloqueio de IP suspeito",
                "severity": "high"
            }
            
            response = client.post(f"{settings.API_V1_STR}/security/threats/{threat_id}/mitigate", json=mitigation_data)
            assert response.status_code == 200
            
            mitigation_result = response.json()
            assert "status" in mitigation_result
            assert "action_taken" in mitigation_result
            assert "timestamp" in mitigation_result
        else:
            # Se não houver ameaças, testar com ID inexistente
            response = client.post(f"{settings.API_V1_STR}/security/threats/99999/mitigate", json={"action": "test"})
            assert response.status_code == 404
    
    async def test_security_audit_log(self, client: TestClient, db_session: AsyncSession):
        """Testar log de auditoria de segurança."""
        
        # Testar log de auditoria
        response = client.get(f"{settings.API_V1_STR}/security/audit")
        assert response.status_code == 200
        
        audit_data = response.json()
        
        # Verificar se é uma lista
        assert isinstance(audit_data, list)
        
        # Se houver logs, verificar estrutura
        if audit_data:
            log_entry = audit_data[0]
            assert "id" in log_entry
            assert "timestamp" in log_entry
            assert "action" in log_entry
            assert "user_id" in log_entry
            assert "resource" in log_entry
            assert "ip_address" in log_entry
            assert "success" in log_entry
    
    async def test_security_audit_with_filters(self, client: TestClient, db_session: AsyncSession):
        """Testar log de auditoria com filtros."""
        
        # Testar filtro por ação
        response = client.get(f"{settings.API_V1_STR}/security/audit?action=login")
        assert response.status_code == 200
        
        login_audits = response.json()
        assert isinstance(login_audits, list)
        
        # Testar filtro por usuário
        response = client.get(f"{settings.API_V1_STR}/security/audit?user_id=1")
        assert response.status_code == 200
        
        user_audits = response.json()
        assert isinstance(user_audits, list)
        
        # Testar filtro por sucesso
        response = client.get(f"{settings.API_V1_STR}/security/audit?success=true")
        assert response.status_code == 200
        
        successful_audits = response.json()
        assert isinstance(successful_audits, list)
        
        # Testar filtro por período
        response = client.get(f"{settings.API_V1_STR}/security/audit?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        
        period_audits = response.json()
        assert isinstance(period_audits, list)
    
    async def test_security_password_validation(self, client: TestClient, db_session: AsyncSession):
        """Testar validação de força de senha."""
        
        # Testar senha fraca
        weak_password_data = {"password": "123"}
        response = client.post(f"{settings.API_V1_STR}/security/validate-password", json=weak_password_data)
        assert response.status_code == 200
        
        weak_result = response.json()
        assert "is_strong" in weak_result
        assert "score" in weak_result
        assert "feedback" in weak_result
        assert weak_result["is_strong"] == False
        assert weak_result["score"] < 50
        
        # Testar senha forte
        strong_password_data = {"password": "MyStr0ng!P@ssw0rd123"}
        response = client.post(f"{settings.API_V1_STR}/security/validate-password", json=strong_password_data)
        assert response.status_code == 200
        
        strong_result = response.json()
        assert strong_result["is_strong"] == True
        assert strong_result["score"] >= 80
        
        # Testar senha média
        medium_password_data = {"password": "Password123"}
        response = client.post(f"{settings.API_V1_STR}/security/validate-password", json=medium_password_data)
        assert response.status_code == 200
        
        medium_result = response.json()
        assert "is_strong" in medium_result
        assert "score" in medium_result
        assert 50 <= medium_result["score"] < 80
    
    async def test_security_cleanup_operations(self, client: TestClient, db_session: AsyncSession):
        """Testar operações de limpeza de segurança."""
        
        # Testar limpeza de dados antigos
        cleanup_data = {
            "days_to_keep": 30,
            "cleanup_types": ["old_events", "old_logs"]
        }
        
        response = client.post(f"{settings.API_V1_STR}/security/cleanup", json=cleanup_data)
        assert response.status_code == 200
        
        cleanup_result = response.json()
        assert "status" in cleanup_result
        assert "items_cleaned" in cleanup_result
        assert "cleanup_date" in cleanup_result
        
        # Verificar se o status é válido
        assert cleanup_result["status"] in ["success", "partial", "failed"]
    
    async def test_security_incident_response(self, client: TestClient, db_session: AsyncSession):
        """Testar resposta a incidentes de segurança."""
        
        # Testar criação de incidente
        incident_data = {
            "title": "Tentativa de Acesso Não Autorizado",
            "description": "Múltiplas tentativas de login falhadas",
            "severity": "high",
            "threat_type": "brute_force",
            "source_ip": "192.168.1.100",
            "affected_resources": ["auth_endpoint", "user_database"]
        }
        
        response = client.post(f"{settings.API_V1_STR}/security/incidents", json=incident_data)
        assert response.status_code == 201
        
        incident = response.json()
        assert incident["title"] == incident_data["title"]
        assert incident["description"] == incident_data["description"]
        assert incident["severity"] == incident_data["severity"]
        assert incident["threat_type"] == incident_data["threat_type"]
        assert incident["status"] == "open"
        
        incident_id = incident["id"]
        
        # Testar atualização de status do incidente
        status_update = {"status": "investigating"}
        response = client.put(f"{settings.API_V1_STR}/security/incidents/{incident_id}", json=status_update)
        assert response.status_code == 200
        
        updated_incident = response.json()
        assert updated_incident["status"] == "investigating"
        
        # Testar resolução do incidente
        resolution_data = {
            "status": "resolved",
            "resolution_notes": "IP bloqueado e usuário notificado"
        }
        
        response = client.put(f"{settings.API_V1_STR}/security/incidents/{incident_id}", json=resolution_data)
        assert response.status_code == 200
        
        resolved_incident = response.json()
        assert resolved_incident["status"] == "resolved"
        assert resolved_incident["resolution_notes"] == resolution_data["resolution_notes"]
    
    async def test_security_validation_errors(self, client: TestClient, db_session: AsyncSession):
        """Testar validação de dados de segurança."""
        
        # Testar dados inválidos para validação de senha
        invalid_password_data = {}
        response = client.post(f"{settings.API_V1_STR}/security/validate-password", json=invalid_password_data)
        assert response.status_code == 422  # Validation Error
        
        # Testar dados inválidos para criação de incidente
        invalid_incident_data = {
            "title": "",  # Título vazio
            "severity": "invalid_severity"  # Severidade inválida
        }
        
        response = client.post(f"{settings.API_V1_STR}/security/incidents", json=invalid_incident_data)
        assert response.status_code == 422  # Validation Error
    
    async def test_security_not_found(self, client: TestClient, db_session: AsyncSession):
        """Testar cenários de recursos de segurança não encontrados."""
        
        # Tentar buscar incidente inexistente
        response = client.get(f"{settings.API_V1_STR}/security/incidents/99999")
        assert response.status_code == 404
        
        # Tentar atualizar incidente inexistente
        update_data = {"status": "resolved"}
        response = client.put(f"{settings.API_V1_STR}/security/incidents/99999", json=update_data)
        assert response.status_code == 404
        
        # Tentar mitigar ameaça inexistente
        mitigation_data = {"action": "block"}
        response = client.post(f"{settings.API_V1_STR}/security/threats/99999/mitigate", json=mitigation_data)
        assert response.status_code == 404
