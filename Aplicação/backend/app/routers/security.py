"""
Security router for security monitoring and management endpoints.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import Session, CurrentUser
from app.security.security_enhancer import SecurityEnhancer, SecurityLevel, ThreatType
from app.middlewares.security import AuthenticationSecurityMiddleware, CSRFProtectionMiddleware

router = APIRouter(
    prefix="/security",
    tags=["security"],
    responses={
        404: {"description": "Recurso não encontrado"},
        400: {"description": "Dados inválidos"},
        401: {"description": "Não autorizado"},
        403: {"description": "Sem permissão"},
        500: {"description": "Erro interno do servidor"}
    }
)

# Global security instances (in production, these should be injected via dependency)
security_enhancer = SecurityEnhancer()
auth_security = AuthenticationSecurityMiddleware(security_enhancer)
csrf_protection = CSRFProtectionMiddleware(security_enhancer)

@router.get(
    "/events",
    response_model=List[Dict[str, Any]],
    summary="Listar Eventos de Segurança",
    description="""
    Lista eventos de segurança recentes com filtros opcionais.
    
    **Parâmetros:**
    - hours: Número de horas para buscar eventos (padrão: 24)
    - severity: Filtrar por nível de severidade (low, medium, high, critical)
    - threat_type: Filtrar por tipo de ameaça
    - limit: Número máximo de eventos (padrão: 100)
    """
)
async def get_security_events(
    session: Session,
    current_user: CurrentUser,
    hours: int = Query(24, ge=1, le=168, description="Hours to look back"),
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    threat_type: Optional[str] = Query(None, description="Filter by threat type"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of events")
):
    """Lista eventos de segurança recentes."""
    try:
        # Convert severity string to enum if provided
        severity_enum = None
        if severity:
            try:
                severity_enum = SecurityLevel(severity.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid severity level: {severity}"
                )
        
        # Convert threat type string to enum if provided
        threat_type_enum = None
        if threat_type:
            try:
                threat_type_enum = ThreatType(threat_type.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid threat type: {threat_type}"
                )
        
        # Get security events
        events = security_enhancer.get_security_events(hours, severity_enum)
        
        # Filter by threat type if specified
        if threat_type_enum:
            events = [e for e in events if e.event_type == threat_type_enum]
        
        # Limit results
        events = events[:limit]
        
        # Convert to response format
        response_events = []
        for event in events:
            response_events.append({
                'timestamp': event.timestamp.isoformat(),
                'event_type': event.event_type.value,
                'severity': event.severity.value,
                'user_id': event.user_id,
                'ip_address': event.ip_address,
                'endpoint': event.endpoint,
                'details': event.details,
                'blocked': event.blocked
            })
        
        return response_events
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/summary",
    response_model=Dict[str, Any],
    summary="Resumo de Segurança",
    description="""
    Obtém resumo estatístico de eventos de segurança.
    
    **Retorna:**
    - Contadores de eventos por tipo e severidade
    - IPs bloqueados
    - Configurações de rate limiting
    - Estatísticas de 24h e 7 dias
    """
)
async def get_security_summary(
    session: Session,
    current_user: CurrentUser
):
    """Obtém resumo de segurança."""
    try:
        summary = security_enhancer.get_security_summary()
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/blocked-ips",
    response_model=List[str],
    summary="Listar IPs Bloqueados",
    description="""
    Lista todos os IPs atualmente bloqueados por ameaças de segurança.
    """
)
async def get_blocked_ips(
    session: Session,
    current_user: CurrentUser
):
    """Lista IPs bloqueados."""
    try:
        return list(security_enhancer.blocked_ips)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/blocked-ips/{ip_address}",
    response_model=Dict[str, str],
    summary="Bloquear IP",
    description="""
    Bloqueia um IP específico por ameaças de segurança.
    
    **Parâmetros:**
    - ip_address: Endereço IP para bloquear
    """
)
async def block_ip(
    ip_address: str,
    session: Session,
    current_user: CurrentUser
):
    """Bloqueia um IP específico."""
    try:
        # Validate IP address format
        import ipaddress
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid IP address format"
            )
        
        # Block the IP
        security_enhancer.blocked_ips.add(ip_address)
        
        # Record security event
        security_enhancer._record_security_event(
            ThreatType.UNAUTHORIZED_ACCESS,
            SecurityLevel.HIGH,
            current_user.id,
            ip_address,
            "/api/v1/security/blocked-ips",
            {
                'action': 'manual_block',
                'blocked_by': current_user.id,
                'reason': 'Manual IP block'
            }
        )
        
        return {"message": f"IP {ip_address} blocked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete(
    "/blocked-ips/{ip_address}",
    response_model=Dict[str, str],
    summary="Desbloquear IP",
    description="""
    Remove o bloqueio de um IP específico.
    
    **Parâmetros:**
    - ip_address: Endereço IP para desbloquear
    """
)
async def unblock_ip(
    ip_address: str,
    session: Session,
    current_user: CurrentUser
):
    """Desbloqueia um IP específico."""
    try:
        # Validate IP address format
        import ipaddress
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid IP address format"
            )
        
        # Unblock the IP
        if ip_address in security_enhancer.blocked_ips:
            security_enhancer.blocked_ips.remove(ip_address)
            
            # Record security event
            security_enhancer._record_security_event(
                ThreatType.UNAUTHORIZED_ACCESS,
                SecurityLevel.LOW,
                current_user.id,
                ip_address,
                "/api/v1/security/blocked-ips",
                {
                    'action': 'manual_unblock',
                    'unblocked_by': current_user.id,
                    'reason': 'Manual IP unblock'
                }
            )
            
            return {"message": f"IP {ip_address} unblocked successfully"}
        else:
            return {"message": f"IP {ip_address} was not blocked"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/rate-limits",
    response_model=Dict[str, Any],
    summary="Status dos Rate Limits",
    description="""
    Obtém status atual dos rate limits para diferentes tipos de endpoint.
    """
)
async def get_rate_limits_status(
    session: Session,
    current_user: CurrentUser
):
    """Obtém status dos rate limits."""
    try:
        rate_limit_status = {}
        
        for endpoint_type, config in security_enhancer.rate_limits.items():
            rate_limit_status[endpoint_type] = {
                'config': config,
                'active_trackers': len([
                    key for key in security_enhancer.rate_limit_tracker.keys()
                    if key.startswith(f"{endpoint_type}:")
                ])
            }
        
        return {
            'rate_limits': rate_limit_status,
            'total_active_trackers': len(security_enhancer.rate_limit_tracker)
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/password-strength",
    response_model=Dict[str, Any],
    summary="Validar Força da Senha",
    description="""
    Valida a força de uma senha sem armazená-la.
    
    **Parâmetros:**
    - password: Senha para validar
    """
)
async def validate_password_strength(
    session: Session,
    current_user: CurrentUser,
    password: str = Query(..., description="Password to validate")
):
    """Valida força da senha."""
    try:
        strength_result = security_enhancer.validate_password_strength(password)
        return strength_result
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/csrf-token",
    response_model=Dict[str, str],
    summary="Gerar Token CSRF",
    description="""
    Gera um token CSRF para proteção contra ataques CSRF.
    """
)
async def generate_csrf_token(
    session: Session,
    current_user: CurrentUser
):
    """Gera token CSRF."""
    try:
        # Use user ID as session identifier
        session_id = str(current_user.id)
        token = csrf_protection.generate_csrf_token(session_id)
        
        return {
            "csrf_token": token,
            "expires_in": csrf_protection.token_expiry
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/login-attempts/{identifier}",
    response_model=Dict[str, Any],
    summary="Status de Tentativas de Login",
    description="""
    Verifica o status de tentativas de login para um usuário ou IP.
    
    **Parâmetros:**
    - identifier: ID do usuário ou endereço IP
    """
)
async def get_login_attempts_status(
    identifier: str,
    session: Session,
    current_user: CurrentUser
):
    """Verifica status de tentativas de login."""
    try:
        # Check if identifier is blocked
        is_allowed = auth_security.check_login_attempts(identifier, identifier)
        lockout_time = auth_security.get_lockout_time(identifier, identifier)
        
        return {
            "identifier": identifier,
            "allowed": is_allowed,
            "lockout_remaining": lockout_time if lockout_time else 0,
            "max_attempts": 5,
            "lockout_duration": auth_security.lockout_duration
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/cleanup",
    response_model=Dict[str, str],
    summary="Limpeza de Dados de Segurança",
    description="""
    Executa limpeza de dados antigos de segurança.
    
    **Parâmetros:**
    - events_days: Dias para manter eventos de segurança (padrão: 30)
    - rate_limits_hours: Horas para manter dados de rate limit (padrão: 24)
    """
)
async def cleanup_security_data(
    session: Session,
    current_user: CurrentUser,
    events_days: int = Query(30, ge=1, le=365, description="Days to keep security events"),
    rate_limits_hours: int = Query(24, ge=1, le=168, description="Hours to keep rate limit data")
):
    """Executa limpeza de dados de segurança."""
    try:
        # Cleanup security events
        security_enhancer.cleanup_old_events(events_days)
        
        # Cleanup rate limit data
        security_enhancer.cleanup_old_rate_limits(rate_limits_hours)
        
        # Cleanup authentication security data
        auth_security.cleanup_old_attempts(24)
        
        # Cleanup CSRF tokens
        csrf_protection.cleanup_expired_tokens()
        
        return {
            "message": f"Security data cleanup completed. Events: {events_days} days, Rate limits: {rate_limits_hours} hours"
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/health",
    response_model=Dict[str, Any],
    summary="Health Check de Segurança",
    description="""
    Verifica a saúde do sistema de segurança.
    """
)
async def security_health_check(
    session: Session,
    current_user: CurrentUser
):
    """Health check do sistema de segurança."""
    try:
        # Get recent security summary
        summary = security_enhancer.get_security_summary()
        
        # Check for critical events in last hour
        critical_events = security_enhancer.get_security_events(1, SecurityLevel.CRITICAL)
        
        # Get recent events for timestamp
        recent_events = security_enhancer.get_security_events(1)
        
        # Determine health status
        health_status = "healthy"
        if len(critical_events) > 0:
            health_status = "warning"
        if len(security_enhancer.blocked_ips) > 100:
            health_status = "critical"
        
        return {
            "status": health_status,
            "blocked_ips_count": len(security_enhancer.blocked_ips),
            "critical_events_last_hour": len(critical_events),
            "total_events_24h": summary["total_events_24h"],
            "active_rate_limits": summary["active_rate_limits"],
            "timestamp": recent_events[0].timestamp.isoformat() if recent_events else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
