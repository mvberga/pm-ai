"""
PDF generator utility for creating project reports and documents.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import io

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Utility class for generating PDF reports and documents."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.darkblue
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='CustomFooter',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
    
    def generate_project_report(self, project_data: Dict[str, Any]) -> bytes:
        """
        Generate a comprehensive project report PDF.
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("Relatório de Projeto", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Project information
        story.append(Paragraph("Informações do Projeto", self.styles['CustomHeading']))
        story.append(self._create_project_info_table(project_data))
        story.append(Spacer(1, 12))
        
        # Team members
        if project_data.get('team_members'):
            story.append(Paragraph("Equipe do Projeto", self.styles['CustomHeading']))
            story.append(self._create_team_table(project_data['team_members']))
            story.append(Spacer(1, 12))
        
        # Clients
        if project_data.get('clients'):
            story.append(Paragraph("Clientes", self.styles['CustomHeading']))
            story.append(self._create_clients_table(project_data['clients']))
            story.append(Spacer(1, 12))
        
        # Risks
        if project_data.get('risks'):
            story.append(Paragraph("Riscos Identificados", self.styles['CustomHeading']))
            story.append(self._create_risks_table(project_data['risks']))
            story.append(Spacer(1, 12))
        
        # Lessons learned
        if project_data.get('lessons_learned'):
            story.append(Paragraph("Lições Aprendidas", self.styles['CustomHeading']))
            story.append(self._create_lessons_table(project_data['lessons_learned']))
            story.append(Spacer(1, 12))
        
        # Next steps
        if project_data.get('next_steps'):
            story.append(Paragraph("Próximos Passos", self.styles['CustomHeading']))
            story.append(self._create_next_steps_table(project_data['next_steps']))
            story.append(Spacer(1, 12))
        
        # Footer
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['CustomFooter']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_risk_report(self, risks_data: List[Dict[str, Any]]) -> bytes:
        """
        Generate a risk assessment report PDF.
        
        Args:
            risks_data: List of risk dictionaries
            
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("Relatório de Análise de Riscos", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Risk summary
        story.append(Paragraph("Resumo dos Riscos", self.styles['CustomHeading']))
        story.append(self._create_risk_summary_table(risks_data))
        story.append(Spacer(1, 12))
        
        # Detailed risks
        story.append(Paragraph("Detalhamento dos Riscos", self.styles['CustomHeading']))
        
        for i, risk in enumerate(risks_data, 1):
            story.append(Paragraph(f"Risco {i}: {risk.get('title', 'N/A')}", self.styles['CustomSubHeading']))
            story.append(self._create_risk_detail_table(risk))
            story.append(Spacer(1, 8))
        
        # Footer
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['CustomFooter']))
        
        doc.build(story)
        return buffer.getvalue()
    
    def generate_team_report(self, team_data: List[Dict[str, Any]]) -> bytes:
        """
        Generate a team report PDF.
        
        Args:
            team_data: List of team member dictionaries
            
        Returns:
            PDF content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("Relatório da Equipe", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Team summary
        story.append(Paragraph("Resumo da Equipe", self.styles['CustomHeading']))
        story.append(self._create_team_summary_table(team_data))
        story.append(Spacer(1, 12))
        
        # Team members by role
        story.append(Paragraph("Membros por Função", self.styles['CustomHeading']))
        story.append(self._create_team_by_role_table(team_data))
        story.append(Spacer(1, 12))
        
        # Detailed team information
        story.append(Paragraph("Informações Detalhadas", self.styles['CustomHeading']))
        story.append(self._create_team_table(team_data))
        
        # Footer
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.styles['CustomFooter']))
        
        doc.build(story)
        return buffer.getvalue()
    
    def _create_project_info_table(self, project_data: Dict[str, Any]) -> Table:
        """Create project information table."""
        data = [
            ['Nome do Projeto', project_data.get('name', 'N/A')],
            ['Descrição', project_data.get('description', 'N/A')],
            ['Status', project_data.get('status', 'N/A')],
            ['Data de Início', project_data.get('start_date', 'N/A')],
            ['Data de Fim', project_data.get('end_date', 'N/A')],
            ['Município', project_data.get('municipio', 'N/A')],
            ['Entidade', project_data.get('entidade', 'N/A')],
            ['Portfólio', project_data.get('portfolio', 'N/A')],
            ['Vertical', project_data.get('vertical', 'N/A')],
            ['Produto', project_data.get('product', 'N/A')],
            ['Valor de Implantação', f"R$ {project_data.get('valor_implantacao', 0):,.2f}"],
            ['Valor Recorrente', f"R$ {project_data.get('valor_recorrente', 0):,.2f}"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_team_table(self, team_data: List[Dict[str, Any]]) -> Table:
        """Create team members table."""
        if not team_data:
            return Table([['Nenhum membro da equipe encontrado']])
        
        headers = ['Nome', 'Email', 'Telefone', 'Cargo', 'Empresa', 'Função']
        data = [headers]
        
        for member in team_data:
            row = [
                member.get('name', 'N/A'),
                member.get('email', 'N/A'),
                member.get('phone', 'N/A'),
                member.get('position', 'N/A'),
                member.get('company', 'N/A'),
                member.get('role', 'N/A')
            ]
            data.append(row)
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_clients_table(self, clients_data: List[Dict[str, Any]]) -> Table:
        """Create clients table."""
        if not clients_data:
            return Table([['Nenhum cliente encontrado']])
        
        headers = ['Nome', 'Empresa', 'Email', 'Telefone', 'Tipo', 'Indústria']
        data = [headers]
        
        for client in clients_data:
            row = [
                client.get('name', 'N/A'),
                client.get('company', 'N/A'),
                client.get('email', 'N/A'),
                client.get('phone', 'N/A'),
                client.get('client_type', 'N/A'),
                client.get('industry', 'N/A')
            ]
            data.append(row)
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_risks_table(self, risks_data: List[Dict[str, Any]]) -> Table:
        """Create risks table."""
        if not risks_data:
            return Table([['Nenhum risco encontrado']])
        
        headers = ['Título', 'Categoria', 'Prioridade', 'Status', 'Probabilidade', 'Impacto']
        data = [headers]
        
        for risk in risks_data:
            row = [
                risk.get('title', 'N/A'),
                risk.get('category', 'N/A'),
                risk.get('priority', 'N/A'),
                risk.get('status', 'N/A'),
                f"{risk.get('probability', 0):.1%}",
                f"{risk.get('impact', 0):.1%}"
            ]
            data.append(row)
        
        table = Table(data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_lessons_table(self, lessons_data: List[Dict[str, Any]]) -> Table:
        """Create lessons learned table."""
        if not lessons_data:
            return Table([['Nenhuma lição aprendida encontrada']])
        
        headers = ['Título', 'Categoria', 'Tipo', 'Data']
        data = [headers]
        
        for lesson in lessons_data:
            row = [
                lesson.get('title', 'N/A'),
                lesson.get('category', 'N/A'),
                lesson.get('lesson_type', 'N/A'),
                lesson.get('lesson_date', 'N/A')
            ]
            data.append(row)
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_next_steps_table(self, next_steps_data: List[Dict[str, Any]]) -> Table:
        """Create next steps table."""
        if not next_steps_data:
            return Table([['Nenhum próximo passo encontrado']])
        
        headers = ['Título', 'Status', 'Prioridade', 'Responsável', 'Data de Vencimento']
        data = [headers]
        
        for step in next_steps_data:
            row = [
                step.get('title', 'N/A'),
                step.get('status', 'N/A'),
                step.get('priority', 'N/A'),
                step.get('assigned_to', 'N/A'),
                step.get('due_date', 'N/A')
            ]
            data.append(row)
        
        table = Table(data, colWidths=[2*inch, 1*inch, 1*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_risk_summary_table(self, risks_data: List[Dict[str, Any]]) -> Table:
        """Create risk summary table."""
        if not risks_data:
            return Table([['Nenhum risco encontrado']])
        
        # Calculate summary statistics
        total_risks = len(risks_data)
        high_priority = len([r for r in risks_data if r.get('priority') == 'high'])
        critical_risks = len([r for r in risks_data if r.get('priority') == 'critical'])
        mitigated_risks = len([r for r in risks_data if r.get('status') == 'mitigated'])
        
        data = [
            ['Total de Riscos', str(total_risks)],
            ['Riscos de Alta Prioridade', str(high_priority)],
            ['Riscos Críticos', str(critical_risks)],
            ['Riscos Mitigados', str(mitigated_risks)],
            ['Taxa de Mitigação', f"{(mitigated_risks/total_risks*100):.1f}%" if total_risks > 0 else "0%"]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_risk_detail_table(self, risk_data: Dict[str, Any]) -> Table:
        """Create detailed risk information table."""
        data = [
            ['Descrição', risk_data.get('description', 'N/A')],
            ['Categoria', risk_data.get('category', 'N/A')],
            ['Probabilidade', f"{risk_data.get('probability', 0):.1%}"],
            ['Impacto', f"{risk_data.get('impact', 0):.1%}"],
            ['Prioridade', risk_data.get('priority', 'N/A')],
            ['Status', risk_data.get('status', 'N/A')],
            ['Causa Raiz', risk_data.get('root_cause', 'N/A')],
            ['Estratégia de Mitigação', risk_data.get('mitigation_strategy', 'N/A')]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_team_summary_table(self, team_data: List[Dict[str, Any]]) -> Table:
        """Create team summary table."""
        if not team_data:
            return Table([['Nenhum membro da equipe encontrado']])
        
        # Calculate summary statistics
        total_members = len(team_data)
        active_members = len([m for m in team_data if m.get('is_active', True)])
        unique_roles = len(set(m.get('role', '') for m in team_data))
        unique_companies = len(set(m.get('company', '') for m in team_data if m.get('company')))
        
        data = [
            ['Total de Membros', str(total_members)],
            ['Membros Ativos', str(active_members)],
            ['Funções Únicas', str(unique_roles)],
            ['Empresas Representadas', str(unique_companies)]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _create_team_by_role_table(self, team_data: List[Dict[str, Any]]) -> Table:
        """Create team members grouped by role table."""
        if not team_data:
            return Table([['Nenhum membro da equipe encontrado']])
        
        # Group by role
        role_groups = {}
        for member in team_data:
            role = member.get('role', 'N/A')
            if role not in role_groups:
                role_groups[role] = []
            role_groups[role].append(member)
        
        data = [['Função', 'Número de Membros', 'Membros']]
        
        for role, members in role_groups.items():
            member_names = ', '.join([m.get('name', 'N/A') for m in members])
            data.append([role, str(len(members)), member_names])
        
        table = Table(data, colWidths=[1.5*inch, 1*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
