"""
Background tasks for AI processing.
"""

from celery import current_task
from app.tasks.celery_app import celery_app
from app.utils.ai_integration import AIIntegration
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def analyze_risk_with_ai(self, risk_data: dict, api_key: str):
    """Analyze risk using AI in background."""
    try:
        # Update task status
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting AI analysis...'})
        
        # Initialize AI integration
        ai = AIIntegration(api_key)
        
        # Analyze risk
        self.update_state(state='PROGRESS', meta={'current': 50, 'total': 100, 'status': 'Analyzing risk...'})
        analysis = ai.analyze_risk(risk_data)
        
        # Complete
        self.update_state(state='PROGRESS', meta={'current': 100, 'total': 100, 'status': 'Analysis completed'})
        
        return {
            'status': 'SUCCESS',
            'message': 'Risk analysis completed',
            'analysis': analysis
        }
        
    except Exception as e:
        logger.error(f"Error analyzing risk with AI: {str(e)}")
        return {'status': 'FAILED', 'error': str(e)}

@celery_app.task(bind=True)
def generate_mitigation_strategy(self, risk_data: dict, api_key: str):
    """Generate mitigation strategy using AI in background."""
    try:
        # Update task status
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Generating strategy...'})
        
        # Initialize AI integration
        ai = AIIntegration(api_key)
        
        # Generate strategy
        self.update_state(state='PROGRESS', meta={'current': 50, 'total': 100, 'status': 'Creating strategy...'})
        strategy = ai.generate_mitigation_strategy(risk_data)
        
        # Complete
        self.update_state(state='PROGRESS', meta={'current': 100, 'total': 100, 'status': 'Strategy generated'})
        
        return {
            'status': 'SUCCESS',
            'message': 'Mitigation strategy generated',
            'strategy': strategy
        }
        
    except Exception as e:
        logger.error(f"Error generating mitigation strategy: {str(e)}")
        return {'status': 'FAILED', 'error': str(e)}
