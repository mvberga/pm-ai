"""
Background tasks for report generation.
"""

from celery import current_task
from app.tasks.celery_app import celery_app
from app.utils.pdf_generator import PDFGenerator
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def generate_project_report(self, project_data: dict, report_type: str = 'project'):
    """Generate project report in background."""
    try:
        # Update task status
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting report generation...'})
        
        # Initialize generator
        generator = PDFGenerator()
        
        # Generate report based on type
        self.update_state(state='PROGRESS', meta={'current': 30, 'total': 100, 'status': 'Generating report...'})
        
        if report_type == 'project':
            pdf_content = generator.generate_project_report(project_data)
        elif report_type == 'risk':
            pdf_content = generator.generate_risk_report(project_data.get('risks', []))
        elif report_type == 'team':
            pdf_content = generator.generate_team_report(project_data.get('team_members', []))
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Complete
        self.update_state(state='PROGRESS', meta={'current': 100, 'total': 100, 'status': 'Report generated'})
        
        return {
            'status': 'SUCCESS',
            'message': 'Report generated successfully',
            'pdf_size': len(pdf_content),
            'report_type': report_type
        }
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return {'status': 'FAILED', 'error': str(e)}
