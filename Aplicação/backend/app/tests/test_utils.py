"""
Tests for utilities.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.utils.excel_parser import ExcelParser
from app.utils.pdf_generator import PDFGenerator
from app.utils.ai_integration import AIIntegration

class TestExcelParser:
    """Test cases for ExcelParser."""
    
    def test_init(self):
        """Test ExcelParser initialization."""
        parser = ExcelParser()
        assert parser.supported_formats == ['.xlsx', '.xls']
    
    def test_parse_date_valid(self):
        """Test parsing valid date."""
        parser = ExcelParser()
        
        # Test with datetime object
        from datetime import datetime
        test_date = datetime(2023, 12, 25)
        result = parser._parse_date(test_date)
        assert result == "2023-12-25T00:00:00"
        
        # Test with string
        result = parser._parse_date("2023-12-25")
        assert result == "2023-12-25T00:00:00"
    
    def test_parse_date_invalid(self):
        """Test parsing invalid date."""
        parser = ExcelParser()
        
        result = parser._parse_date("invalid_date")
        assert result is None
        
        result = parser._parse_date(None)
        assert result is None
    
    def test_parse_float_valid(self):
        """Test parsing valid float."""
        parser = ExcelParser()
        
        result = parser._parse_float("123.45")
        assert result == 123.45
        
        result = parser._parse_float("R$ 1,234.56")
        assert result == 1234.56
    
    def test_parse_float_invalid(self):
        """Test parsing invalid float."""
        parser = ExcelParser()
        
        result = parser._parse_float("invalid")
        assert result is None
        
        result = parser._parse_float(None)
        assert result is None

class TestPDFGenerator:
    """Test cases for PDFGenerator."""
    
    def test_init(self):
        """Test PDFGenerator initialization."""
        generator = PDFGenerator()
        assert generator.styles is not None
        assert 'CustomTitle' in generator.styles.byName
    
    def test_generate_project_report(self):
        """Test generating project report."""
        generator = PDFGenerator()
        
        project_data = {
            'name': 'Test Project',
            'description': 'Test Description',
            'status': 'active',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'municipio': 'Test City',
            'entidade': 'Test Entity',
            'portfolio': 'Test Portfolio',
            'vertical': 'Test Vertical',
            'product': 'Test Product',
            'valor_implantacao': 100000.0,
            'valor_recorrente': 10000.0,
            'team_members': [],
            'clients': [],
            'risks': [],
            'lessons_learned': [],
            'next_steps': []
        }
        
        pdf_content = generator.generate_project_report(project_data)
        
        assert isinstance(pdf_content, bytes)
        assert len(pdf_content) > 0
    
    def test_generate_risk_report(self):
        """Test generating risk report."""
        generator = PDFGenerator()
        
        risks_data = [
            {
                'title': 'Test Risk',
                'description': 'Test Description',
                'category': 'technical',
                'probability': 0.5,
                'impact': 0.7,
                'priority': 'high',
                'status': 'identified'
            }
        ]
        
        pdf_content = generator.generate_risk_report(risks_data)
        
        assert isinstance(pdf_content, bytes)
        assert len(pdf_content) > 0

class TestAIIntegration:
    """Test cases for AIIntegration."""
    
    def test_init(self):
        """Test AIIntegration initialization."""
        ai = AIIntegration("test_api_key")
        assert ai.api_key == "test_api_key"
        assert ai.model is not None
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation."""
        ai = AIIntegration("test_api_key")
        
        risk_data = {
            'title': 'Test Risk',
            'description': 'Test Description',
            'category': 'technical',
            'probability': 0.5,
            'impact': 0.7
        }
        
        score = ai._calculate_confidence_score(risk_data)
        assert 0.0 <= score <= 1.0
    
    def test_calculate_health_score(self):
        """Test project health score calculation."""
        ai = AIIntegration("test_api_key")
        
        project_data = {
            'status': 'on_track',
            'risks': [],
            'team_members': []
        }
        
        score = ai._calculate_health_score(project_data)
        assert 0.0 <= score <= 1.0
    
    def test_extract_recommendations(self):
        """Test extracting recommendations from text."""
        ai = AIIntegration("test_api_key")
        
        text = "Recomendo implementar testes. Sugiro melhorar documentação."
        recommendations = ai._extract_recommendations(text)
        
        assert len(recommendations) > 0
        assert any("recomendo" in rec.lower() for rec in recommendations)
    
    def test_extract_action_items(self):
        """Test extracting action items from text."""
        ai = AIIntegration("test_api_key")
        
        text = "Implementar testes unitários. Executar análise de código."
        action_items = ai._extract_action_items(text)
        
        assert len(action_items) > 0
        assert any("implementar" in item.lower() for item in action_items)
