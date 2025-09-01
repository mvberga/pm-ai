export interface Project {
  id: number;
  name: string;
  municipio: string;
  entidade?: string;
  chamado_jira?: string;
  portfolio?: string;
  vertical?: string;
  product?: string;
  tipo: string;
  data_inicio: string;
  data_fim: string;
  etapa_atual?: string;
  valor_implantacao: number;
  valor_recorrente: number;
  recursos: number;
  status: string;
  gerente_projeto_id: number;
  gerente_portfolio_id: number;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioMetrics {
  total_projects: number;
  total_implantation: number;
  total_recurring: number;
  total_resources: number;
  projects_by_status: Record<string, number>;
  projects_by_municipio: Record<string, number>;
  projects_by_portfolio: Record<string, number>;
}

export interface ProjectTask {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  status: string;
  assignee_id?: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectImplantador {
  id: number;
  project_id: number;
  user_id: number;
  role?: string;
  created_at: string;
}

export interface ProjectMigrador {
  id: number;
  project_id: number;
  user_id: number;
  role?: string;
  created_at: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export type ProjectStatus = 'not_started' | 'on_track' | 'warning' | 'delayed' | 'completed';
export type ProjectType = 'implantacao' | 'migracao' | 'configuracao' | 'treinamento' | 'suporte';
