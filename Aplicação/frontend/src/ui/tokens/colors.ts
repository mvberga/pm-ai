// Tokens de design baseados no HTML unificado
export const colors = {
  // Cores principais da Betha
  primary: {
    50: '#eff6ff',
    100: '#dbeafe', 
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#0761FF', // Cor principal da Betha
    600: '#054ed9',
    700: '#1d4ed8',
    800: '#1e40af',
    900: '#1e3a8a',
  },
  
  // Cores secundárias
  secondary: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    200: '#bae6fd',
    300: '#7dd3fc',
    400: '#38bdf8',
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
    800: '#075985',
    900: '#0c4a6e',
  },
  
  // Cores de status
  status: {
    success: '#10b981',
    warning: '#f59e0b', 
    error: '#ef4444',
    info: '#3b82f6',
  },
  
  // Cores de fundo (dark theme)
  background: {
    primary: '#0f172a',    // slate-900
    secondary: '#1e293b',  // slate-800
    tertiary: '#334155',   // slate-700
    card: '#1e293b',       // slate-800
    sidebar: '#0f172a',    // slate-900
  },
  
  // Cores de texto
  text: {
    primary: '#f1f5f9',    // slate-100
    secondary: '#94a3b8',  // slate-400
    tertiary: '#64748b',   // slate-500
    muted: '#475569',      // slate-600
  },
  
  // Cores de borda
  border: {
    primary: '#334155',    // slate-700
    secondary: '#475569',  // slate-600
    focus: '#0761FF',      // primary-500
  },
  
  // Cores específicas para action items
  actionItems: {
    pending: '#f59e0b',    // warning
    inProgress: '#3b82f6', // info
    completed: '#10b981',  // success
    cancelled: '#ef4444',  // error
    onHold: '#6b7280',     // gray-500
  },
  
  // Cores específicas para prioridades
  priority: {
    low: '#10b981',        // success
    medium: '#f59e0b',     // warning
    high: '#f97316',       // orange-500
    critical: '#ef4444',   // error
  },
  
  // Cores específicas para tipos de action items
  actionTypes: {
    technical: '#8b5cf6',   // violet-500
    business: '#06b6d4',    // cyan-500
    communication: '#84cc16', // lime-500
    documentation: '#f59e0b', // warning
    testing: '#ec4899',     // pink-500
    deployment: '#10b981',  // success
    training: '#3b82f6',    // info
    support: '#6b7280',     // gray-500
  }
} as const;

// Utilitários para cores
export const getStatusColor = (status: string) => {
  const statusMap: Record<string, string> = {
    'not_started': colors.text.tertiary,
    'on_track': colors.status.success,
    'warning': colors.status.warning,
    'delayed': colors.status.error,
    'completed': colors.status.success,
  };
  return statusMap[status] || colors.text.secondary;
};

export const getActionItemStatusColor = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': colors.actionItems.pending,
    'in_progress': colors.actionItems.inProgress,
    'completed': colors.actionItems.completed,
    'cancelled': colors.actionItems.cancelled,
    'on_hold': colors.actionItems.onHold,
  };
  return statusMap[status] || colors.text.secondary;
};

export const getPriorityColor = (priority: string) => {
  const priorityMap: Record<string, string> = {
    'low': colors.priority.low,
    'medium': colors.priority.medium,
    'high': colors.priority.high,
    'critical': colors.priority.critical,
  };
  return priorityMap[priority] || colors.text.secondary;
};

export const getActionTypeColor = (type: string) => {
  const typeMap: Record<string, string> = {
    'technical': colors.actionTypes.technical,
    'business': colors.actionTypes.business,
    'communication': colors.actionTypes.communication,
    'documentation': colors.actionTypes.documentation,
    'testing': colors.actionTypes.testing,
    'deployment': colors.actionTypes.deployment,
    'training': colors.actionTypes.training,
    'support': colors.actionTypes.support,
  };
  return typeMap[type] || colors.text.secondary;
};
