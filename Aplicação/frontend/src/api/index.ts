// API Client
export { default as api } from './client';

// Projects API
export { projectsApi, useProjects, useProjectsMetrics } from './projects';
export type { ProjectCreateRequest, ProjectUpdateRequest } from './projects';

// Action Items API
export { actionItemsApi, useActionItems } from './actionItems';

// Portfolios API
export { portfoliosApi, usePortfolios, usePortfolio } from './portfolios';

// Team Members API
export { teamMembersApi, useTeamMembers, useTeamMember } from './teamMembers';

// Clients API
export { clientsApi, useClients, useClient } from './clients';

// Risks API
export { risksApi, useRisks, useRisk, useRiskAnalysis } from './risks';