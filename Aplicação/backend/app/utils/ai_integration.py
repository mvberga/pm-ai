"""
AI integration utility for Gemini API integration.
"""

import google.generativeai as genai
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AIIntegration:
    """Utility class for AI integration with Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize AI integration with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_risk(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a risk using AI and provide recommendations.
        
        Args:
            risk_data: Dictionary containing risk information
            
        Returns:
            Dictionary with AI analysis and recommendations
        """
        try:
            prompt = self._create_risk_analysis_prompt(risk_data)
            response = self.model.generate_content(prompt)
            
            analysis = {
                'risk_id': risk_data.get('id'),
                'ai_analysis': response.text,
                'confidence_score': self._calculate_confidence_score(risk_data),
                'generated_at': datetime.now().isoformat(),
                'recommendations': self._extract_recommendations(response.text)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing risk with AI: {str(e)}")
            return {
                'risk_id': risk_data.get('id'),
                'ai_analysis': f"Erro na análise: {str(e)}",
                'confidence_score': 0.0,
                'generated_at': datetime.now().isoformat(),
                'recommendations': []
            }
    
    def generate_mitigation_strategy(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mitigation strategy for a risk.
        
        Args:
            risk_data: Dictionary containing risk information
            
        Returns:
            Dictionary with mitigation strategy
        """
        try:
            prompt = self._create_mitigation_strategy_prompt(risk_data)
            response = self.model.generate_content(prompt)
            
            strategy = {
                'risk_id': risk_data.get('id'),
                'mitigation_strategy': response.text,
                'generated_at': datetime.now().isoformat(),
                'action_items': self._extract_action_items(response.text)
            }
            
            return strategy
            
        except Exception as e:
            logger.error(f"Error generating mitigation strategy: {str(e)}")
            return {
                'risk_id': risk_data.get('id'),
                'mitigation_strategy': f"Erro na geração de estratégia: {str(e)}",
                'generated_at': datetime.now().isoformat(),
                'action_items': []
            }
    
    def analyze_project_health(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze overall project health using AI.
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            Dictionary with project health analysis
        """
        try:
            prompt = self._create_project_health_prompt(project_data)
            response = self.model.generate_content(prompt)
            
            analysis = {
                'project_id': project_data.get('id'),
                'health_score': self._calculate_health_score(project_data),
                'analysis': response.text,
                'generated_at': datetime.now().isoformat(),
                'recommendations': self._extract_recommendations(response.text),
                'risk_factors': self._identify_risk_factors(project_data)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing project health: {str(e)}")
            return {
                'project_id': project_data.get('id'),
                'health_score': 0.0,
                'analysis': f"Erro na análise: {str(e)}",
                'generated_at': datetime.now().isoformat(),
                'recommendations': [],
                'risk_factors': []
            }
    
    def generate_lessons_learned(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate lessons learned insights from project data.
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            Dictionary with lessons learned insights
        """
        try:
            prompt = self._create_lessons_learned_prompt(project_data)
            response = self.model.generate_content(prompt)
            
            lessons = {
                'project_id': project_data.get('id'),
                'insights': response.text,
                'generated_at': datetime.now().isoformat(),
                'key_lessons': self._extract_key_lessons(response.text),
                'best_practices': self._extract_best_practices(response.text)
            }
            
            return lessons
            
        except Exception as e:
            logger.error(f"Error generating lessons learned: {str(e)}")
            return {
                'project_id': project_data.get('id'),
                'insights': f"Erro na geração de insights: {str(e)}",
                'generated_at': datetime.now().isoformat(),
                'key_lessons': [],
                'best_practices': []
            }
    
    def generate_next_steps(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate next steps recommendations for a project.
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            Dictionary with next steps recommendations
        """
        try:
            prompt = self._create_next_steps_prompt(project_data)
            response = self.model.generate_content(prompt)
            
            next_steps = {
                'project_id': project_data.get('id'),
                'recommendations': response.text,
                'generated_at': datetime.now().isoformat(),
                'action_items': self._extract_action_items(response.text),
                'priorities': self._extract_priorities(response.text)
            }
            
            return next_steps
            
        except Exception as e:
            logger.error(f"Error generating next steps: {str(e)}")
            return {
                'project_id': project_data.get('id'),
                'recommendations': f"Erro na geração de recomendações: {str(e)}",
                'generated_at': datetime.now().isoformat(),
                'action_items': [],
                'priorities': []
            }
    
    def _create_risk_analysis_prompt(self, risk_data: Dict[str, Any]) -> str:
        """Create prompt for risk analysis."""
        return f"""
        Analise o seguinte risco de projeto e forneça uma análise detalhada:

        Título: {risk_data.get('title', 'N/A')}
        Descrição: {risk_data.get('description', 'N/A')}
        Categoria: {risk_data.get('category', 'N/A')}
        Probabilidade: {risk_data.get('probability', 0)}
        Impacto: {risk_data.get('impact', 0)}
        Prioridade: {risk_data.get('priority', 'N/A')}
        Status: {risk_data.get('status', 'N/A')}
        Causa Raiz: {risk_data.get('root_cause', 'N/A')}

        Por favor, forneça:
        1. Análise detalhada do risco
        2. Fatores que contribuem para o risco
        3. Impacto potencial no projeto
        4. Recomendações para mitigação
        5. Indicadores de monitoramento

        Responda em português brasileiro.
        """
    
    def _create_mitigation_strategy_prompt(self, risk_data: Dict[str, Any]) -> str:
        """Create prompt for mitigation strategy generation."""
        return f"""
        Gere uma estratégia de mitigação para o seguinte risco:

        Título: {risk_data.get('title', 'N/A')}
        Descrição: {risk_data.get('description', 'N/A')}
        Categoria: {risk_data.get('category', 'N/A')}
        Probabilidade: {risk_data.get('probability', 0)}
        Impacto: {risk_data.get('impact', 0)}
        Causa Raiz: {risk_data.get('root_cause', 'N/A')}

        Por favor, forneça:
        1. Estratégia de mitigação detalhada
        2. Plano de ação específico
        3. Responsáveis pelas ações
        4. Cronograma de implementação
        5. Indicadores de sucesso

        Responda em português brasileiro.
        """
    
    def _create_project_health_prompt(self, project_data: Dict[str, Any]) -> str:
        """Create prompt for project health analysis."""
        return f"""
        Analise a saúde geral do seguinte projeto:

        Nome: {project_data.get('name', 'N/A')}
        Status: {project_data.get('status', 'N/A')}
        Data de Início: {project_data.get('start_date', 'N/A')}
        Data de Fim: {project_data.get('end_date', 'N/A')}
        Descrição: {project_data.get('description', 'N/A')}

        Equipe: {len(project_data.get('team_members', []))} membros
        Clientes: {len(project_data.get('clients', []))} clientes
        Riscos: {len(project_data.get('risks', []))} riscos identificados
        Lições Aprendidas: {len(project_data.get('lessons_learned', []))} lições
        Próximos Passos: {len(project_data.get('next_steps', []))} itens

        Por favor, forneça:
        1. Análise geral da saúde do projeto
        2. Pontos fortes identificados
        3. Áreas de melhoria
        4. Recomendações prioritárias
        5. Indicadores de sucesso

        Responda em português brasileiro.
        """
    
    def _create_lessons_learned_prompt(self, project_data: Dict[str, Any]) -> str:
        """Create prompt for lessons learned generation."""
        return f"""
        Gere insights de lições aprendidas para o seguinte projeto:

        Nome: {project_data.get('name', 'N/A')}
        Status: {project_data.get('status', 'N/A')}
        Descrição: {project_data.get('description', 'N/A')}

        Riscos identificados: {len(project_data.get('risks', []))}
        Lições já documentadas: {len(project_data.get('lessons_learned', []))}
        Próximos passos: {len(project_data.get('next_steps', []))}

        Por favor, forneça:
        1. Lições aprendidas principais
        2. Melhores práticas identificadas
        3. O que funcionou bem
        4. O que poderia ser melhorado
        5. Recomendações para projetos futuros

        Responda em português brasileiro.
        """
    
    def _create_next_steps_prompt(self, project_data: Dict[str, Any]) -> str:
        """Create prompt for next steps generation."""
        return f"""
        Gere recomendações de próximos passos para o seguinte projeto:

        Nome: {project_data.get('name', 'N/A')}
        Status: {project_data.get('status', 'N/A')}
        Data de Fim: {project_data.get('end_date', 'N/A')}
        Descrição: {project_data.get('description', 'N/A')}

        Riscos ativos: {len([r for r in project_data.get('risks', []) if r.get('status') != 'mitigated'])}
        Próximos passos pendentes: {len([s for s in project_data.get('next_steps', []) if s.get('status') == 'pending'])}

        Por favor, forneça:
        1. Próximos passos prioritários
        2. Ações recomendadas
        3. Cronograma sugerido
        4. Responsáveis indicados
        5. Marcos importantes

        Responda em português brasileiro.
        """
    
    def _calculate_confidence_score(self, risk_data: Dict[str, Any]) -> float:
        """Calculate confidence score for risk analysis."""
        try:
            # Base confidence on data completeness
            required_fields = ['title', 'description', 'category', 'probability', 'impact']
            filled_fields = sum(1 for field in required_fields if risk_data.get(field) is not None)
            base_confidence = filled_fields / len(required_fields)
            
            # Adjust based on risk complexity
            complexity_factor = 1.0
            if risk_data.get('probability', 0) > 0.7 or risk_data.get('impact', 0) > 0.7:
                complexity_factor = 0.8  # Lower confidence for high-risk items
            
            return min(base_confidence * complexity_factor, 1.0)
        except Exception:
            return 0.5
    
    def _calculate_health_score(self, project_data: Dict[str, Any]) -> float:
        """Calculate project health score."""
        try:
            score = 0.0
            total_factors = 0
            
            # Status factor
            status = project_data.get('status', '')
            if status == 'completed':
                score += 1.0
            elif status == 'on_track':
                score += 0.8
            elif status == 'warning':
                score += 0.6
            elif status == 'delayed':
                score += 0.4
            else:
                score += 0.2
            total_factors += 1
            
            # Risk factor
            risks = project_data.get('risks', [])
            if not risks:
                score += 1.0
            else:
                mitigated_risks = len([r for r in risks if r.get('status') == 'mitigated'])
                risk_score = mitigated_risks / len(risks) if risks else 1.0
                score += risk_score
            total_factors += 1
            
            # Team factor
            team_members = project_data.get('team_members', [])
            if team_members:
                active_members = len([m for m in team_members if m.get('is_active', True)])
                team_score = active_members / len(team_members)
                score += team_score
            else:
                score += 0.5  # Neutral score if no team data
            total_factors += 1
            
            return score / total_factors if total_factors > 0 else 0.5
        except Exception:
            return 0.5
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from AI response text."""
        try:
            recommendations = []
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['recomendo', 'sugiro', 'recomendação', 'sugestão']):
                    recommendations.append(line)
            
            return recommendations[:5]  # Limit to 5 recommendations
        except Exception:
            return []
    
    def _extract_action_items(self, text: str) -> List[str]:
        """Extract action items from AI response text."""
        try:
            action_items = []
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['ação', 'tarefa', 'implementar', 'executar']):
                    action_items.append(line)
            
            return action_items[:5]  # Limit to 5 action items
        except Exception:
            return []
    
    def _extract_key_lessons(self, text: str) -> List[str]:
        """Extract key lessons from AI response text."""
        try:
            lessons = []
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['lição', 'aprendizado', 'insight', 'descoberta']):
                    lessons.append(line)
            
            return lessons[:5]  # Limit to 5 lessons
        except Exception:
            return []
    
    def _extract_best_practices(self, text: str) -> List[str]:
        """Extract best practices from AI response text."""
        try:
            practices = []
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['melhor prática', 'boa prática', 'eficaz', 'funcionou bem']):
                    practices.append(line)
            
            return practices[:5]  # Limit to 5 practices
        except Exception:
            return []
    
    def _extract_priorities(self, text: str) -> List[str]:
        """Extract priorities from AI response text."""
        try:
            priorities = []
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['prioridade', 'urgente', 'importante', 'crítico']):
                    priorities.append(line)
            
            return priorities[:5]  # Limit to 5 priorities
        except Exception:
            return []
    
    def _identify_risk_factors(self, project_data: Dict[str, Any]) -> List[str]:
        """Identify risk factors from project data."""
        try:
            risk_factors = []
            
            # Check for common risk factors
            if not project_data.get('team_members'):
                risk_factors.append("Falta de membros da equipe definidos")
            
            if not project_data.get('clients'):
                risk_factors.append("Falta de informações do cliente")
            
            risks = project_data.get('risks', [])
            high_priority_risks = [r for r in risks if r.get('priority') in ['high', 'critical']]
            if high_priority_risks:
                risk_factors.append(f"{len(high_priority_risks)} riscos de alta prioridade")
            
            overdue_steps = [s for s in project_data.get('next_steps', []) if s.get('status') == 'pending' and s.get('due_date')]
            if overdue_steps:
                risk_factors.append(f"{len(overdue_steps)} próximos passos em atraso")
            
            return risk_factors
        except Exception:
            return []
