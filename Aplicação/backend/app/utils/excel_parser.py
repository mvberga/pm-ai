"""
Excel parser utility for processing project data from spreadsheets.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ExcelParser:
    """Utility class for parsing Excel files and extracting project data."""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls']
    
    def parse_project_spreadsheet(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a project spreadsheet and extract structured data.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dictionary containing parsed project data
        """
        try:
            # Read all sheets from the Excel file
            excel_file = pd.ExcelFile(file_path)
            parsed_data = {
                'file_info': {
                    'filename': file_path.split('/')[-1],
                    'sheets': excel_file.sheet_names,
                    'parsed_at': datetime.now().isoformat()
                },
                'projects': [],
                'team_members': [],
                'clients': [],
                'risks': [],
                'errors': []
            }
            
            # Parse each sheet
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    sheet_data = self._parse_sheet(sheet_name, df)
                    
                    if sheet_data:
                        parsed_data.update(sheet_data)
                        
                except Exception as e:
                    error_msg = f"Error parsing sheet '{sheet_name}': {str(e)}"
                    logger.error(error_msg)
                    parsed_data['errors'].append(error_msg)
            
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing Excel file: {str(e)}")
            return {
                'file_info': {'filename': file_path.split('/')[-1]},
                'projects': [],
                'team_members': [],
                'clients': [],
                'risks': [],
                'errors': [f"Failed to parse file: {str(e)}"]
            }
    
    def _parse_sheet(self, sheet_name: str, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Parse a specific sheet based on its name and content.
        
        Args:
            sheet_name: Name of the sheet
            df: DataFrame containing sheet data
            
        Returns:
            Dictionary with parsed data or None if sheet is not recognized
        """
        sheet_name_lower = sheet_name.lower()
        
        if 'projeto' in sheet_name_lower or 'project' in sheet_name_lower:
            return {'projects': self._parse_projects_sheet(df)}
        elif 'equipe' in sheet_name_lower or 'team' in sheet_name_lower:
            return {'team_members': self._parse_team_sheet(df)}
        elif 'cliente' in sheet_name_lower or 'client' in sheet_name_lower:
            return {'clients': self._parse_clients_sheet(df)}
        elif 'risco' in sheet_name_lower or 'risk' in sheet_name_lower:
            return {'risks': self._parse_risks_sheet(df)}
        else:
            # Try to auto-detect based on column names
            return self._auto_detect_sheet_type(df)
    
    def _parse_projects_sheet(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Parse projects sheet."""
        projects = []
        
        # Map common column names to standard fields
        column_mapping = {
            'nome': 'name',
            'name': 'name',
            'projeto': 'name',
            'descrição': 'description',
            'description': 'description',
            'descricao': 'description',
            'município': 'municipio',
            'municipio': 'municipio',
            'cidade': 'municipio',
            'city': 'municipio',
            'entidade': 'entidade',
            'entity': 'entidade',
            'status': 'status',
            'data_início': 'start_date',
            'data_inicio': 'start_date',
            'start_date': 'start_date',
            'data_fim': 'end_date',
            'end_date': 'end_date',
            'valor_implantação': 'valor_implantacao',
            'valor_implantacao': 'valor_implantacao',
            'valor_recorrente': 'valor_recorrente',
            'portfolio': 'portfolio',
            'portfólio': 'portfolio',
            'vertical': 'vertical',
            'produto': 'product',
            'product': 'product',
            'tipo': 'tipo',
            'type': 'tipo'
        }
        
        # Rename columns to standard names
        df_renamed = df.rename(columns=column_mapping)
        
        for _, row in df_renamed.iterrows():
            try:
                project = {
                    'name': str(row.get('name', '')),
                    'description': str(row.get('description', '')),
                    'municipio': str(row.get('municipio', '')),
                    'entidade': str(row.get('entidade', '')),
                    'status': str(row.get('status', 'not_started')),
                    'start_date': self._parse_date(row.get('start_date')),
                    'end_date': self._parse_date(row.get('end_date')),
                    'valor_implantacao': self._parse_float(row.get('valor_implantacao')),
                    'valor_recorrente': self._parse_float(row.get('valor_recorrente')),
                    'portfolio': str(row.get('portfolio', '')),
                    'vertical': str(row.get('vertical', '')),
                    'product': str(row.get('product', '')),
                    'tipo': str(row.get('tipo', 'implantacao'))
                }
                
                # Remove empty values
                project = {k: v for k, v in project.items() if v != '' and v is not None}
                projects.append(project)
                
            except Exception as e:
                logger.error(f"Error parsing project row: {str(e)}")
                continue
        
        return projects
    
    def _parse_team_sheet(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Parse team members sheet."""
        team_members = []
        
        column_mapping = {
            'nome': 'name',
            'name': 'name',
            'email': 'email',
            'telefone': 'phone',
            'phone': 'phone',
            'cargo': 'position',
            'position': 'position',
            'empresa': 'company',
            'company': 'company',
            'função': 'role',
            'role': 'role',
            'responsabilidades': 'responsibilities',
            'responsibilities': 'responsibilities'
        }
        
        df_renamed = df.rename(columns=column_mapping)
        
        for _, row in df_renamed.iterrows():
            try:
                team_member = {
                    'name': str(row.get('name', '')),
                    'email': str(row.get('email', '')),
                    'phone': str(row.get('phone', '')),
                    'position': str(row.get('position', '')),
                    'company': str(row.get('company', '')),
                    'role': str(row.get('role', 'stakeholder')),
                    'responsibilities': str(row.get('responsibilities', ''))
                }
                
                # Remove empty values
                team_member = {k: v for k, v in team_member.items() if v != '' and v is not None}
                team_members.append(team_member)
                
            except Exception as e:
                logger.error(f"Error parsing team member row: {str(e)}")
                continue
        
        return team_members
    
    def _parse_clients_sheet(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Parse clients sheet."""
        clients = []
        
        column_mapping = {
            'nome': 'name',
            'name': 'name',
            'empresa': 'company',
            'company': 'company',
            'email': 'email',
            'telefone': 'phone',
            'phone': 'phone',
            'endereço': 'address',
            'address': 'address',
            'website': 'website',
            'contato_principal': 'primary_contact',
            'primary_contact': 'primary_contact',
            'tipo': 'client_type',
            'client_type': 'client_type',
            'indústria': 'industry',
            'industry': 'industry'
        }
        
        df_renamed = df.rename(columns=column_mapping)
        
        for _, row in df_renamed.iterrows():
            try:
                client = {
                    'name': str(row.get('name', '')),
                    'company': str(row.get('company', '')),
                    'email': str(row.get('email', '')),
                    'phone': str(row.get('phone', '')),
                    'address': str(row.get('address', '')),
                    'website': str(row.get('website', '')),
                    'primary_contact': str(row.get('primary_contact', '')),
                    'client_type': str(row.get('client_type', 'corporate')),
                    'industry': str(row.get('industry', ''))
                }
                
                # Remove empty values
                client = {k: v for k, v in client.items() if v != '' and v is not None}
                clients.append(client)
                
            except Exception as e:
                logger.error(f"Error parsing client row: {str(e)}")
                continue
        
        return clients
    
    def _parse_risks_sheet(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Parse risks sheet."""
        risks = []
        
        column_mapping = {
            'título': 'title',
            'title': 'title',
            'descrição': 'description',
            'description': 'description',
            'categoria': 'category',
            'category': 'category',
            'probabilidade': 'probability',
            'probability': 'probability',
            'impacto': 'impact',
            'impact': 'impact',
            'prioridade': 'priority',
            'priority': 'priority',
            'status': 'status',
            'causa_raiz': 'root_cause',
            'root_cause': 'root_cause',
            'estratégia_mitigação': 'mitigation_strategy',
            'mitigation_strategy': 'mitigation_strategy'
        }
        
        df_renamed = df.rename(columns=column_mapping)
        
        for _, row in df_renamed.iterrows():
            try:
                risk = {
                    'title': str(row.get('title', '')),
                    'description': str(row.get('description', '')),
                    'category': str(row.get('category', 'technical')),
                    'probability': self._parse_float(row.get('probability', 0.5)),
                    'impact': self._parse_float(row.get('impact', 0.5)),
                    'priority': str(row.get('priority', 'medium')),
                    'status': str(row.get('status', 'identified')),
                    'root_cause': str(row.get('root_cause', '')),
                    'mitigation_strategy': str(row.get('mitigation_strategy', ''))
                }
                
                # Remove empty values
                risk = {k: v for k, v in risk.items() if v != '' and v is not None}
                risks.append(risk)
                
            except Exception as e:
                logger.error(f"Error parsing risk row: {str(e)}")
                continue
        
        return risks
    
    def _auto_detect_sheet_type(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Auto-detect sheet type based on column names."""
        columns_lower = [col.lower() for col in df.columns]
        
        # Check for project indicators
        project_indicators = ['nome', 'name', 'projeto', 'project', 'município', 'municipio', 'cidade']
        if any(indicator in columns_lower for indicator in project_indicators):
            return {'projects': self._parse_projects_sheet(df)}
        
        # Check for team indicators
        team_indicators = ['equipe', 'team', 'membro', 'member', 'cargo', 'position']
        if any(indicator in columns_lower for indicator in team_indicators):
            return {'team_members': self._parse_team_sheet(df)}
        
        # Check for client indicators
        client_indicators = ['cliente', 'client', 'empresa', 'company', 'contato', 'contact']
        if any(indicator in columns_lower for indicator in client_indicators):
            return {'clients': self._parse_clients_sheet(df)}
        
        # Check for risk indicators
        risk_indicators = ['risco', 'risk', 'probabilidade', 'probability', 'impacto', 'impact']
        if any(indicator in columns_lower for indicator in risk_indicators):
            return {'risks': self._parse_risks_sheet(df)}
        
        return None
    
    def _parse_date(self, value: Any) -> Optional[str]:
        """Parse date value to ISO format string."""
        if pd.isna(value) or value == '':
            return None
        
        try:
            if isinstance(value, datetime):
                return value.isoformat()
            elif isinstance(value, str):
                # Try to parse common date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']:
                    try:
                        parsed_date = datetime.strptime(value, fmt)
                        return parsed_date.isoformat()
                    except ValueError:
                        continue
            return None
        except Exception:
            return None
    
    def _parse_float(self, value: Any) -> Optional[float]:
        """Parse float value."""
        if pd.isna(value) or value == '':
            return None
        
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                # Remove common currency symbols and commas
                cleaned = value.replace('R$', '').replace(',', '').replace('$', '').strip()
                return float(cleaned)
            return None
        except Exception:
            return None
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate Excel file before parsing.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        try:
            # Check file extension
            if not any(file_path.lower().endswith(ext) for ext in self.supported_formats):
                validation_result['is_valid'] = False
                validation_result['errors'].append(f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}")
                return validation_result
            
            # Try to read the file
            excel_file = pd.ExcelFile(file_path)
            validation_result['file_info'] = {
                'filename': file_path.split('/')[-1],
                'sheets': excel_file.sheet_names,
                'sheet_count': len(excel_file.sheet_names)
            }
            
            # Check for empty sheets
            for sheet_name in excel_file.sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    if df.empty:
                        validation_result['warnings'].append(f"Sheet '{sheet_name}' is empty")
                except Exception as e:
                    validation_result['warnings'].append(f"Could not read sheet '{sheet_name}': {str(e)}")
            
        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"File validation failed: {str(e)}")
        
        return validation_result
