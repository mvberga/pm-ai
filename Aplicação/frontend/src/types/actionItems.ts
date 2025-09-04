export interface ActionItem {
  id: number;
  project_id: number;
  title: string;
  description?: string;
  type: ActionItemType;
  status: ActionItemStatus;
  priority: ActionItemPriority;
  assignee_id?: number;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export type ActionItemType = 
  | 'technical' 
  | 'business' 
  | 'communication' 
  | 'documentation' 
  | 'testing' 
  | 'deployment'
  | 'training'
  | 'support';

export type ActionItemStatus = 
  | 'pending' 
  | 'in_progress' 
  | 'completed' 
  | 'cancelled'
  | 'on_hold';

export type ActionItemPriority = 
  | 'low' 
  | 'medium' 
  | 'high' 
  | 'critical';

export interface ActionItemFilters {
  type?: ActionItemType;
  status?: ActionItemStatus;
  priority?: ActionItemPriority;
  project_id?: number;
}

export interface ActionItemCreateRequest {
  project_id: number;
  title: string;
  description?: string;
  type: ActionItemType;
  priority: ActionItemPriority;
  assignee_id?: number;
  due_date?: string;
}

export interface ActionItemUpdateRequest {
  title?: string;
  description?: string;
  type?: ActionItemType;
  status?: ActionItemStatus;
  priority?: ActionItemPriority;
  assignee_id?: number;
  due_date?: string;
}

// Tipos para estatísticas e KPIs
export interface ActionItemStats {
  total: number;
  pending: number;
  in_progress: number;
  completed: number;
  cancelled: number;
  on_hold: number;
  by_type: Record<ActionItemType, number>;
  by_priority: Record<ActionItemPriority, number>;
}

export interface ProjectActionItemSummary {
  project_id: number;
  project_name: string;
  total_actions: number;
  pending_actions: number;
  completed_actions: number;
  overdue_actions: number;
}
