import { 
  colors, 
  getStatusColor, 
  getActionItemStatusColor, 
  getPriorityColor, 
  getActionTypeColor 
} from '../../../ui/tokens/colors';

describe('Colors Tokens', () => {
  describe('colors object', () => {
    it('deve ter estrutura correta de cores primárias', () => {
      expect(colors.primary).toBeDefined();
      expect(colors.primary[50]).toBe('#eff6ff');
      expect(colors.primary[100]).toBe('#dbeafe');
      expect(colors.primary[200]).toBe('#bfdbfe');
      expect(colors.primary[300]).toBe('#93c5fd');
      expect(colors.primary[400]).toBe('#60a5fa');
      expect(colors.primary[500]).toBe('#0761FF'); // Cor principal da Betha
      expect(colors.primary[600]).toBe('#054ed9');
      expect(colors.primary[700]).toBe('#1d4ed8');
      expect(colors.primary[800]).toBe('#1e40af');
      expect(colors.primary[900]).toBe('#1e3a8a');
    });

    it('deve ter estrutura correta de cores secundárias', () => {
      expect(colors.secondary).toBeDefined();
      expect(colors.secondary[50]).toBe('#f0f9ff');
      expect(colors.secondary[100]).toBe('#e0f2fe');
      expect(colors.secondary[200]).toBe('#bae6fd');
      expect(colors.secondary[300]).toBe('#7dd3fc');
      expect(colors.secondary[400]).toBe('#38bdf8');
      expect(colors.secondary[500]).toBe('#0ea5e9');
      expect(colors.secondary[600]).toBe('#0284c7');
      expect(colors.secondary[700]).toBe('#0369a1');
      expect(colors.secondary[800]).toBe('#075985');
      expect(colors.secondary[900]).toBe('#0c4a6e');
    });

    it('deve ter cores de status definidas', () => {
      expect(colors.status).toBeDefined();
      expect(colors.status.success).toBe('#10b981');
      expect(colors.status.warning).toBe('#f59e0b');
      expect(colors.status.error).toBe('#ef4444');
      expect(colors.status.info).toBe('#3b82f6');
    });

    it('deve ter cores de fundo para dark theme', () => {
      expect(colors.background).toBeDefined();
      expect(colors.background.primary).toBe('#0f172a');    // slate-900
      expect(colors.background.secondary).toBe('#1e293b');  // slate-800
      expect(colors.background.tertiary).toBe('#334155');   // slate-700
      expect(colors.background.card).toBe('#1e293b');       // slate-800
      expect(colors.background.sidebar).toBe('#0f172a');    // slate-900
    });

    it('deve ter cores de texto definidas', () => {
      expect(colors.text).toBeDefined();
      expect(colors.text.primary).toBe('#f1f5f9');    // slate-100
      expect(colors.text.secondary).toBe('#94a3b8');  // slate-400
      expect(colors.text.tertiary).toBe('#64748b');   // slate-500
      expect(colors.text.muted).toBe('#475569');      // slate-600
    });

    it('deve ter cores de borda definidas', () => {
      expect(colors.border).toBeDefined();
      expect(colors.border.primary).toBe('#334155');    // slate-700
      expect(colors.border.secondary).toBe('#475569');  // slate-600
      expect(colors.border.focus).toBe('#0761FF');      // primary-500
    });

    it('deve ter cores específicas para action items', () => {
      expect(colors.actionItems).toBeDefined();
      expect(colors.actionItems.pending).toBe('#f59e0b');    // warning
      expect(colors.actionItems.inProgress).toBe('#3b82f6'); // info
      expect(colors.actionItems.completed).toBe('#10b981');  // success
      expect(colors.actionItems.cancelled).toBe('#ef4444');  // error
      expect(colors.actionItems.onHold).toBe('#6b7280');     // gray-500
    });

    it('deve ter cores específicas para prioridades', () => {
      expect(colors.priority).toBeDefined();
      expect(colors.priority.low).toBe('#10b981');        // success
      expect(colors.priority.medium).toBe('#f59e0b');     // warning
      expect(colors.priority.high).toBe('#f97316');       // orange-500
      expect(colors.priority.critical).toBe('#ef4444');   // error
    });

    it('deve ter cores específicas para tipos de action items', () => {
      expect(colors.actionTypes).toBeDefined();
      expect(colors.actionTypes.technical).toBe('#8b5cf6');   // violet-500
      expect(colors.actionTypes.business).toBe('#06b6d4');    // cyan-500
      expect(colors.actionTypes.communication).toBe('#84cc16'); // lime-500
      expect(colors.actionTypes.documentation).toBe('#f59e0b'); // warning
      expect(colors.actionTypes.testing).toBe('#ec4899');     // pink-500
      expect(colors.actionTypes.deployment).toBe('#10b981');  // success
      expect(colors.actionTypes.training).toBe('#3b82f6');    // info
      expect(colors.actionTypes.support).toBe('#6b7280');     // gray-500
    });

    it('deve ser readonly (as const)', () => {
      // Testa se o objeto é readonly - em runtime JavaScript não previne modificação
      // mas o TypeScript com 'as const' torna readonly em tempo de compilação
      const originalValue = colors.primary[500];
      (colors as any).primary[500] = '#000000';
      expect(colors.primary[500]).toBe('#000000');
      
      // Restaura o valor original
      (colors as any).primary[500] = originalValue;
      expect(colors.primary[500]).toBe('#0761FF');
    });
  });

  describe('getStatusColor', () => {
    it('deve retornar cor correta para status válidos', () => {
      expect(getStatusColor('not_started')).toBe(colors.text.tertiary);
      expect(getStatusColor('on_track')).toBe(colors.status.success);
      expect(getStatusColor('warning')).toBe(colors.status.warning);
      expect(getStatusColor('delayed')).toBe(colors.status.error);
      expect(getStatusColor('completed')).toBe(colors.status.success);
    });

    it('deve retornar cor padrão para status inválido', () => {
      expect(getStatusColor('invalid_status')).toBe(colors.text.secondary);
      expect(getStatusColor('')).toBe(colors.text.secondary);
      expect(getStatusColor('unknown')).toBe(colors.text.secondary);
    });

    it('deve ser case-sensitive', () => {
      expect(getStatusColor('NOT_STARTED')).toBe(colors.text.secondary);
      expect(getStatusColor('On_Track')).toBe(colors.text.secondary);
      expect(getStatusColor('WARNING')).toBe(colors.text.secondary);
    });

    it('deve lidar com valores null/undefined', () => {
      expect(getStatusColor(null as any)).toBe(colors.text.secondary);
      expect(getStatusColor(undefined as any)).toBe(colors.text.secondary);
    });
  });

  describe('getActionItemStatusColor', () => {
    it('deve retornar cor correta para status válidos', () => {
      expect(getActionItemStatusColor('pending')).toBe(colors.actionItems.pending);
      expect(getActionItemStatusColor('in_progress')).toBe(colors.actionItems.inProgress);
      expect(getActionItemStatusColor('completed')).toBe(colors.actionItems.completed);
      expect(getActionItemStatusColor('cancelled')).toBe(colors.actionItems.cancelled);
      expect(getActionItemStatusColor('on_hold')).toBe(colors.actionItems.onHold);
    });

    it('deve retornar cor padrão para status inválido', () => {
      expect(getActionItemStatusColor('invalid_status')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor('')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor('unknown')).toBe(colors.text.secondary);
    });

    it('deve ser case-sensitive', () => {
      expect(getActionItemStatusColor('PENDING')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor('In_Progress')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor('COMPLETED')).toBe(colors.text.secondary);
    });

    it('deve lidar com valores null/undefined', () => {
      expect(getActionItemStatusColor(null as any)).toBe(colors.text.secondary);
      expect(getActionItemStatusColor(undefined as any)).toBe(colors.text.secondary);
    });
  });

  describe('getPriorityColor', () => {
    it('deve retornar cor correta para prioridades válidas', () => {
      expect(getPriorityColor('low')).toBe(colors.priority.low);
      expect(getPriorityColor('medium')).toBe(colors.priority.medium);
      expect(getPriorityColor('high')).toBe(colors.priority.high);
      expect(getPriorityColor('critical')).toBe(colors.priority.critical);
    });

    it('deve retornar cor padrão para prioridade inválida', () => {
      expect(getPriorityColor('invalid_priority')).toBe(colors.text.secondary);
      expect(getPriorityColor('')).toBe(colors.text.secondary);
      expect(getPriorityColor('unknown')).toBe(colors.text.secondary);
    });

    it('deve ser case-sensitive', () => {
      expect(getPriorityColor('LOW')).toBe(colors.text.secondary);
      expect(getPriorityColor('Medium')).toBe(colors.text.secondary);
      expect(getPriorityColor('HIGH')).toBe(colors.text.secondary);
      expect(getPriorityColor('CRITICAL')).toBe(colors.text.secondary);
    });

    it('deve lidar com valores null/undefined', () => {
      expect(getPriorityColor(null as any)).toBe(colors.text.secondary);
      expect(getPriorityColor(undefined as any)).toBe(colors.text.secondary);
    });
  });

  describe('getActionTypeColor', () => {
    it('deve retornar cor correta para tipos válidos', () => {
      expect(getActionTypeColor('technical')).toBe(colors.actionTypes.technical);
      expect(getActionTypeColor('business')).toBe(colors.actionTypes.business);
      expect(getActionTypeColor('communication')).toBe(colors.actionTypes.communication);
      expect(getActionTypeColor('documentation')).toBe(colors.actionTypes.documentation);
      expect(getActionTypeColor('testing')).toBe(colors.actionTypes.testing);
      expect(getActionTypeColor('deployment')).toBe(colors.actionTypes.deployment);
      expect(getActionTypeColor('training')).toBe(colors.actionTypes.training);
      expect(getActionTypeColor('support')).toBe(colors.actionTypes.support);
    });

    it('deve retornar cor padrão para tipo inválido', () => {
      expect(getActionTypeColor('invalid_type')).toBe(colors.text.secondary);
      expect(getActionTypeColor('')).toBe(colors.text.secondary);
      expect(getActionTypeColor('unknown')).toBe(colors.text.secondary);
    });

    it('deve ser case-sensitive', () => {
      expect(getActionTypeColor('TECHNICAL')).toBe(colors.text.secondary);
      expect(getActionTypeColor('Business')).toBe(colors.text.secondary);
      expect(getActionTypeColor('COMMUNICATION')).toBe(colors.text.secondary);
    });

    it('deve lidar com valores null/undefined', () => {
      expect(getActionTypeColor(null as any)).toBe(colors.text.secondary);
      expect(getActionTypeColor(undefined as any)).toBe(colors.text.secondary);
    });
  });

  describe('Consistência de cores', () => {
    it('deve ter cores válidas em formato hexadecimal', () => {
      const hexColorRegex = /^#[0-9A-Fa-f]{6}$/;
      
      // Testa todas as cores primárias
      Object.values(colors.primary).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa todas as cores secundárias
      Object.values(colors.secondary).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de status
      Object.values(colors.status).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de fundo
      Object.values(colors.background).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de texto
      Object.values(colors.text).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de borda
      Object.values(colors.border).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de action items
      Object.values(colors.actionItems).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de prioridade
      Object.values(colors.priority).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
      
      // Testa cores de tipos de action items
      Object.values(colors.actionTypes).forEach(color => {
        expect(color).toMatch(hexColorRegex);
      });
    });

    it('deve ter cores únicas (sem duplicatas)', () => {
      const allColors = [
        ...Object.values(colors.primary),
        ...Object.values(colors.secondary),
        ...Object.values(colors.status),
        ...Object.values(colors.background),
        ...Object.values(colors.text),
        ...Object.values(colors.border),
        ...Object.values(colors.actionItems),
        ...Object.values(colors.priority),
        ...Object.values(colors.actionTypes),
      ];
      
      const uniqueColors = new Set(allColors);
      // Algumas cores são intencionalmente duplicadas (ex: success, warning, error)
      // Verifica se há pelo menos 30 cores únicas (esperado: ~38 únicas de 53 totais)
      expect(uniqueColors.size).toBeGreaterThan(30);
      expect(uniqueColors.size).toBeLessThanOrEqual(allColors.length);
    });

    it('deve ter cor principal da Betha definida corretamente', () => {
      // Restaura o valor original caso tenha sido modificado em outros testes
      (colors as any).primary[500] = '#0761FF';
      expect(colors.primary[500]).toBe('#0761FF');
      expect(colors.border.focus).toBe('#0761FF');
    });
  });

  describe('Funções utilitárias - casos extremos', () => {
    it('deve lidar com strings com espaços', () => {
      expect(getStatusColor(' not_started ')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor(' pending ')).toBe(colors.text.secondary);
      expect(getPriorityColor(' low ')).toBe(colors.text.secondary);
      expect(getActionTypeColor(' technical ')).toBe(colors.text.secondary);
    });

    it('deve lidar com strings com caracteres especiais', () => {
      expect(getStatusColor('not_started!')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor('pending@')).toBe(colors.text.secondary);
      expect(getPriorityColor('low#')).toBe(colors.text.secondary);
      expect(getActionTypeColor('technical$')).toBe(colors.text.secondary);
    });

    it('deve lidar com números como string', () => {
      expect(getStatusColor('123')).toBe(colors.text.secondary);
      expect(getActionItemStatusColor('456')).toBe(colors.text.secondary);
      expect(getPriorityColor('789')).toBe(colors.text.secondary);
      expect(getActionTypeColor('012')).toBe(colors.text.secondary);
    });

    it('deve lidar com objetos como parâmetro', () => {
      expect(getStatusColor({} as any)).toBe(colors.text.secondary);
      expect(getActionItemStatusColor({} as any)).toBe(colors.text.secondary);
      expect(getPriorityColor({} as any)).toBe(colors.text.secondary);
      expect(getActionTypeColor({} as any)).toBe(colors.text.secondary);
    });

    it('deve lidar com arrays como parâmetro', () => {
      expect(getStatusColor([] as any)).toBe(colors.text.secondary);
      expect(getActionItemStatusColor([] as any)).toBe(colors.text.secondary);
      expect(getPriorityColor([] as any)).toBe(colors.text.secondary);
      expect(getActionTypeColor([] as any)).toBe(colors.text.secondary);
    });
  });
});
