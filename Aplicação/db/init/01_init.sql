-- Enable pgvector extension (already present in the image)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create users table (if not exists)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create projects table with all required fields
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Localização e Organização
    municipio VARCHAR(100) NOT NULL,
    entidade VARCHAR(100),
    
    -- Rastreamento
    chamado_jira VARCHAR(50),
    
    -- Categorização
    portfolio VARCHAR(100),
    vertical VARCHAR(100),
    product VARCHAR(100),
    tipo VARCHAR(50) DEFAULT 'implantacao',
    
    -- Cronograma
    data_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    data_fim TIMESTAMP WITH TIME ZONE NOT NULL,
    etapa_atual VARCHAR(100),
    
    -- Financeiro
    valor_implantacao DECIMAL(15,2) DEFAULT 0.0,
    valor_recorrente DECIMAL(15,2) DEFAULT 0.0,
    
    -- Status e Recursos
    status VARCHAR(50) DEFAULT 'not_started',
    recursos INTEGER DEFAULT 0,
    
    -- Responsáveis
    gerente_projeto_id INTEGER REFERENCES users(id),
    gerente_portfolio_id INTEGER REFERENCES users(id),
    owner_id INTEGER REFERENCES users(id),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create project_members table
CREATE TABLE IF NOT EXISTS project_members (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create project_implantadores table
CREATE TABLE IF NOT EXISTS project_implantadores (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create project_migradores table
CREATE TABLE IF NOT EXISTS project_migradores (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create project_tasks table
CREATE TABLE IF NOT EXISTS project_tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) DEFAULT 'not_started',
    assignee_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_projects_municipio ON projects(municipio);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_portfolio ON projects(portfolio);
CREATE INDEX IF NOT EXISTS idx_projects_vertical ON projects(vertical);
CREATE INDEX IF NOT EXISTS idx_projects_data_inicio ON projects(data_inicio);
CREATE INDEX IF NOT EXISTS idx_projects_data_fim ON projects(data_fim);
CREATE INDEX IF NOT EXISTS idx_projects_gerente_projeto ON projects(gerente_projeto_id);
CREATE INDEX IF NOT EXISTS idx_projects_gerente_portfolio ON projects(gerente_portfolio_id);

CREATE INDEX IF NOT EXISTS idx_project_members_project_id ON project_members(project_id);
CREATE INDEX IF NOT EXISTS idx_project_implantadores_project_id ON project_implantadores(project_id);
CREATE INDEX IF NOT EXISTS idx_project_migradores_project_id ON project_migradores(project_id);
CREATE INDEX IF NOT EXISTS idx_project_tasks_project_id ON project_tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_project_tasks_status ON project_tasks(status);

-- Insert sample users
INSERT INTO users (email, name) VALUES 
    ('vitor.vargas@betha.com.br', 'Vitor Vargas'),
    ('marcos.bergamaschi@betha.com.br', 'Marcos Bergamaschi'),
    ('leandro.faveri@betha.com.br', 'Leandro de Faveri'),
    ('maxwell.santos@betha.com.br', 'Maxwell Santos')
ON CONFLICT (email) DO NOTHING;

-- Insert sample projects (based on the mockup data)
INSERT INTO projects (
    name, description, municipio, entidade, chamado_jira,
    portfolio, vertical, product, tipo, data_inicio, data_fim,
    etapa_atual, valor_implantacao, valor_recorrente, recursos,
    gerente_projeto_id, gerente_portfolio_id, owner_id, status
) VALUES 
    (
        'Lagoa Santa - Notas e Livro',
        'Sistema de notas fiscais e livro eletrônico para PM Lagoa Santa',
        'Lagoa Santa',
        'Prefeitura Municipal',
        'JIRA-001',
        'Premium SC/MG',
        'Arrecadação',
        'e-Nota + Livro Eletrônico',
        'implantacao',
        '2025-08-13 00:00:00+00',
        '2025-10-24 00:00:00+00',
        'Migração de Homologação',
        13000.00,
        15000.00,
        4,
        1, -- Vitor Vargas
        3, -- Leandro de Faveri
        1, -- Vitor Vargas
        'on_track'
    ),
    (
        'Jaraguá do Sul - Protocolo Samae',
        'Sistema de protocolo para SAMAE de Jaraguá do Sul',
        'Jaraguá do Sul',
        'SAMAE',
        'JIRA-002',
        'Premium SC/MG',
        'Protocolo',
        'Protocolo Cloud',
        'implantacao',
        '2025-08-13 00:00:00+00',
        '2025-09-15 00:00:00+00',
        'Migração em Produção',
        4000.00,
        0.00,
        3,
        2, -- Marcos Bergamaschi
        3, -- Leandro de Faveri
        2, -- Marcos Bergamaschi
        'warning'
    ),
    (
        'Major Gercino',
        'Sistema completo para PM Major Gercino',
        'Major Gercino',
        'Prefeitura Municipal',
        'JIRA-003',
        'Premium SC/MG',
        'Tributos',
        'Beth Tributos',
        'implantacao',
        '2025-07-10 00:00:00+00',
        '2025-09-15 00:00:00+00',
        'Operação assistida',
        61172.62,
        0.00,
        8,
        1, -- Vitor Vargas
        3, -- Leandro de Faveri
        1, -- Vitor Vargas
        'on_track'
    )
ON CONFLICT (id) DO NOTHING;

-- Insert sample project tasks
INSERT INTO project_tasks (
    project_id, name, description, start_date, end_date, status, assignee_id
) VALUES 
    (1, 'Planejamento e Monitoramento', 'Fase inicial de planejamento', '2025-08-13 00:00:00+00', '2025-10-24 00:00:00+00', 'in_progress', 1),
    (1, 'Kickoff', 'Reunião de início do projeto', '2025-08-22 00:00:00+00', '2025-08-22 00:00:00+00', 'completed', 1),
    (1, 'Diagnóstico', 'Análise da base atual', '2025-08-13 00:00:00+00', '2025-08-29 00:00:00+00', 'completed', 1),
    (1, 'Migração de Homologação', 'Migração para ambiente de homologação', '2025-08-13 00:00:00+00', '2025-09-05 00:00:00+00', 'in_progress', 1),
    
    (2, 'Planejamento e Monitoramento', 'Fase inicial de planejamento', '2025-08-13 00:00:00+00', '2025-10-24 00:00:00+00', 'in_progress', 2),
    (2, 'Kick-Off', 'Reunião de início do projeto', '2025-08-10 00:00:00+00', '2025-08-10 00:00:00+00', 'completed', 2),
    (2, 'Diagnóstico', 'Análise da base atual', '2025-08-13 00:00:00+00', '2025-08-29 00:00:00+00', 'completed', 2),
    
    (3, 'Planejamento e Monitoramento', 'Fase inicial de planejamento', '2025-07-10 00:00:00+00', '2025-09-15 00:00:00+00', 'in_progress', 1),
    (3, 'Kick-Off', 'Reunião de início do projeto', '2025-07-10 00:00:00+00', '2025-07-10 00:00:00+00', 'completed', 1),
    (3, 'Diagnóstico', 'Análise da base atual', '2025-07-21 00:00:00+00', '2025-07-28 00:00:00+00', 'completed', 1)
ON CONFLICT (id) DO NOTHING;

-- Insert sample project implantadores
INSERT INTO project_implantadores (project_id, user_id, role) VALUES 
    (1, 1, 'Gerente de Projeto'),
    (2, 2, 'Gerente de Projeto'),
    (3, 1, 'Gerente de Projeto')
ON CONFLICT (id) DO NOTHING;
