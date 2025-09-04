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

// Tipos expandidos para a página de status
export interface ProjectWithActions extends Project {
  action_items_count?: number;
  pending_actions_count?: number;
  completed_actions_count?: number;
  overdue_actions_count?: number;
}

export interface ProjectFilters {
  status?: string;
  portfolio?: string;
  vertical?: string;
  municipio?: string;
  search?: string;
}

export interface ProjectStats {
  total_projects: number;
  projects_by_status: Record<string, number>;
  projects_by_portfolio: Record<string, number>;
  projects_by_vertical: Record<string, number>;
  projects_by_municipio: Record<string, number>;
  total_implantation_value: number;
  total_recurring_value: number;
  total_resources: number;
  projects_with_pending_actions: number;
  projects_with_overdue_actions: number;
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

// ===== NOVOS TIPOS PARA INTEGRAÇÃO COM BACKEND EXPANDIDO =====

// Portfolio Types
export interface Portfolio {
  id: number;
  name: string;
  description?: string;
  owner_id: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface PortfolioCreate {
  name: string;
  description?: string;
  is_active?: boolean;
}

export interface PortfolioUpdate {
  name?: string;
  description?: string;
  is_active?: boolean;
}

export interface PortfolioSummary {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  projects_count: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioWithProjects extends Portfolio {
  projects: Project[];
}

// Team Member Types
export type TeamRole = 'project_manager' | 'developer' | 'designer' | 'analyst' | 'tester' | 'consultant';

export interface TeamMember {
  id: number;
  project_id: number;
  name: string;
  email: string;
  role: TeamRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TeamMemberCreate {
  project_id: number;
  name: string;
  email: string;
  role: TeamRole;
  is_active?: boolean;
}

export interface TeamMemberUpdate {
  name?: string;
  email?: string;
  role?: TeamRole;
  is_active?: boolean;
}

export interface TeamMemberSummary {
  id: number;
  name: string;
  email: string;
  role: TeamRole;
  is_active: boolean;
  created_at: string;
}

export interface TeamMemberBulkCreate {
  project_id: number;
  members: Omit<TeamMemberCreate, 'project_id'>[];
}

export interface TeamMemberBulkUpdate {
  members: Array<{
    id: number;
    data: TeamMemberUpdate;
  }>;
}

// Client Types
export type ClientType = 'internal' | 'external' | 'government' | 'private';
export type CommunicationLevel = 'low' | 'medium' | 'high' | 'critical';

export interface Client {
  id: number;
  project_id: number;
  name: string;
  email: string;
  client_type: ClientType;
  communication_level: CommunicationLevel;
  created_at: string;
  updated_at: string;
}

export interface ClientCreate {
  project_id: number;
  name: string;
  email: string;
  client_type: ClientType;
  communication_level: CommunicationLevel;
}

export interface ClientUpdate {
  name?: string;
  email?: string;
  client_type?: ClientType;
  communication_level?: CommunicationLevel;
}

export interface ClientResponse {
  id: number;
  project_id: number;
  name: string;
  email: string;
  client_type: ClientType;
  communication_level: CommunicationLevel;
  created_at: string;
  updated_at: string;
}

export interface ClientSummary {
  id: number;
  name: string;
  email: string;
  client_type: ClientType;
  communication_level: CommunicationLevel;
  created_at: string;
}

export interface ClientBulkCreate {
  project_id: number;
  clients: Omit<ClientCreate, 'project_id'>[];
}

export interface ClientBulkUpdate {
  clients: Array<{
    id: number;
    data: ClientUpdate;
  }>;
}

// Risk Types
export type RiskCategory = 'technical' | 'business' | 'operational' | 'financial' | 'legal' | 'environmental';
export type RiskStatus = 'identified' | 'assessed' | 'mitigated' | 'monitored' | 'closed';
export type RiskPriority = 'low' | 'medium' | 'high' | 'critical';

export interface Risk {
  id: number;
  project_id: number;
  title: string;
  description: string;
  category: RiskCategory;
  status: RiskStatus;
  priority: RiskPriority;
  probability: number;
  impact: number;
  mitigation_plan?: string;
  owner_id?: number;
  created_at: string;
  updated_at: string;
}

export interface RiskCreate {
  project_id: number;
  title: string;
  description: string;
  category: RiskCategory;
  status?: RiskStatus;
  priority: RiskPriority;
  probability: number;
  impact: number;
  mitigation_plan?: string;
  owner_id?: number;
}

export interface RiskUpdate {
  title?: string;
  description?: string;
  category?: RiskCategory;
  status?: RiskStatus;
  priority?: RiskPriority;
  probability?: number;
  impact?: number;
  mitigation_plan?: string;
  owner_id?: number;
}

export interface RiskResponse {
  id: number;
  project_id: number;
  title: string;
  description: string;
  category: RiskCategory;
  status: RiskStatus;
  priority: RiskPriority;
  probability: number;
  impact: number;
  mitigation_plan?: string;
  owner_id?: number;
  created_at: string;
  updated_at: string;
}

export interface RiskSummary {
  id: number;
  title: string;
  category: RiskCategory;
  status: RiskStatus;
  priority: RiskPriority;
  probability: number;
  impact: number;
  created_at: string;
}

export interface RiskAnalysis {
  total_risks: number;
  risks_by_category: Record<RiskCategory, number>;
  risks_by_status: Record<RiskStatus, number>;
  risks_by_priority: Record<RiskPriority, number>;
  high_impact_risks: RiskSummary[];
  overdue_risks: RiskSummary[];
}

export interface RiskBulkCreate {
  project_id: number;
  risks: Omit<RiskCreate, 'project_id'>[];
}

export interface RiskBulkUpdate {
  risks: Array<{
    id: number;
    data: RiskUpdate;
  }>;
}

// Lesson Learned Types
export type LessonCategory = 'technical' | 'process' | 'communication' | 'management' | 'quality' | 'delivery';
export type LessonType = 'success' | 'failure' | 'improvement' | 'best_practice';

export interface LessonLearned {
  id: number;
  project_id: number;
  title: string;
  description: string;
  category: LessonCategory;
  lesson_type: LessonType;
  impact: string;
  recommendations: string;
  created_at: string;
  updated_at: string;
}

export interface LessonLearnedCreate {
  project_id: number;
  title: string;
  description: string;
  category: LessonCategory;
  lesson_type: LessonType;
  impact: string;
  recommendations: string;
}

export interface LessonLearnedUpdate {
  title?: string;
  description?: string;
  category?: LessonCategory;
  lesson_type?: LessonType;
  impact?: string;
  recommendations?: string;
}

export interface LessonLearnedResponse {
  id: number;
  project_id: number;
  title: string;
  description: string;
  category: LessonCategory;
  lesson_type: LessonType;
  impact: string;
  recommendations: string;
  created_at: string;
  updated_at: string;
}

export interface LessonLearnedSummary {
  id: number;
  title: string;
  category: LessonCategory;
  lesson_type: LessonType;
  impact: string;
  created_at: string;
}

export interface LessonLearnedAnalysis {
  total_lessons: number;
  lessons_by_category: Record<LessonCategory, number>;
  lessons_by_type: Record<LessonType, number>;
  recent_lessons: LessonLearnedSummary[];
  top_categories: Array<{
    category: LessonCategory;
    count: number;
  }>;
}

export interface LessonLearnedBulkCreate {
  project_id: number;
  lessons: Omit<LessonLearnedCreate, 'project_id'>[];
}

export interface LessonLearnedBulkUpdate {
  lessons: Array<{
    id: number;
    data: LessonLearnedUpdate;
  }>;
}

// Next Step Types
export type NextStepStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled';
export type NextStepPriority = 'low' | 'medium' | 'high' | 'urgent';
export type NextStepType = 'action' | 'decision' | 'review' | 'delivery' | 'meeting';

export interface NextStep {
  id: number;
  project_id: number;
  title: string;
  description: string;
  status: NextStepStatus;
  priority: NextStepPriority;
  step_type: NextStepType;
  due_date?: string;
  assignee_id?: number;
  created_at: string;
  updated_at: string;
}

export interface NextStepCreate {
  project_id: number;
  title: string;
  description: string;
  status?: NextStepStatus;
  priority: NextStepPriority;
  step_type: NextStepType;
  due_date?: string;
  assignee_id?: number;
}

export interface NextStepUpdate {
  title?: string;
  description?: string;
  status?: NextStepStatus;
  priority?: NextStepPriority;
  step_type?: NextStepType;
  due_date?: string;
  assignee_id?: number;
}

export interface NextStepResponse {
  id: number;
  project_id: number;
  title: string;
  description: string;
  status: NextStepStatus;
  priority: NextStepPriority;
  step_type: NextStepType;
  due_date?: string;
  assignee_id?: number;
  created_at: string;
  updated_at: string;
}

export interface NextStepSummary {
  id: number;
  title: string;
  status: NextStepStatus;
  priority: NextStepPriority;
  step_type: NextStepType;
  due_date?: string;
  created_at: string;
}

export interface NextStepAnalysis {
  total_steps: number;
  steps_by_status: Record<NextStepStatus, number>;
  steps_by_priority: Record<NextStepPriority, number>;
  steps_by_type: Record<NextStepType, number>;
  overdue_steps: NextStepSummary[];
  upcoming_steps: NextStepSummary[];
}

export interface NextStepBulkCreate {
  project_id: number;
  steps: Omit<NextStepCreate, 'project_id'>[];
}

export interface NextStepBulkUpdate {
  steps: Array<{
    id: number;
    data: NextStepUpdate;
  }>;
}