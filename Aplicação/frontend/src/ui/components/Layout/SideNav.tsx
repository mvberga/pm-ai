import React from 'react';
import { colors } from '../../tokens/colors';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  href: string;
  badge?: number;
  isActive?: boolean;
}

interface SideNavProps {
  items: NavItem[];
  onItemClick?: (item: NavItem) => void;
  className?: string;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
}

export const SideNav: React.FC<SideNavProps> = ({
  items,
  onItemClick,
  className = "",
  isCollapsed = false,
  onToggleCollapse
}) => {
  const handleItemClick = (item: NavItem) => {
    if (onItemClick) {
      onItemClick(item);
    }
  };

  return (
    <aside className={`bg-slate-900 shadow-lg flex-shrink-0 flex flex-col ${className}`}>
      {/* Header da sidebar */}
      <div className="p-6 flex items-center border-b border-slate-700">
        <img 
          src="data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3e%3crect width='100' height='100' rx='20' fill='%230761FF'/%3e%3ctext x='50' y='55' font-family='Inter, sans-serif' font-size='75' font-weight='bold' fill='white' text-anchor='middle' dominant-baseline='middle'%3eB%3c/text%3e%3c/svg%3e" 
          alt="Betha Logo" 
          className="w-10 h-10 mr-3 rounded"
        />
        {!isCollapsed && (
          <div className="flex flex-col">
            <span className="text-white font-bold text-lg">Betha Sistemas</span>
            <span className="text-sm text-slate-400">Gerenciamento</span>
          </div>
        )}
        
        {/* Botão para colapsar/expandir */}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="ml-auto p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label={isCollapsed ? "Expandir menu" : "Colapsar menu"}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d={isCollapsed ? "M9 5l7 7-7 7" : "M15 19l-7-7 7-7"} 
              />
            </svg>
          </button>
        )}
      </div>

      {/* Navegação */}
      <nav className="mt-6 flex-grow">
        <ul className="space-y-1 px-3">
          {items.map((item) => (
            <li key={item.id}>
              <a
                href={item.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleItemClick(item);
                }}
                className={`
                  flex items-center px-3 py-3 text-white rounded-lg transition-colors
                  ${item.isActive 
                    ? 'bg-primary-600 font-semibold' 
                    : 'hover:bg-primary-600/50'
                  }
                  ${isCollapsed ? 'justify-center' : ''}
                `}
                title={isCollapsed ? item.label : undefined}
              >
                <span className={`${isCollapsed ? '' : 'mr-3'}`}>
                  {item.icon}
                </span>
                {!isCollapsed && (
                  <>
                    <span className="flex-1">{item.label}</span>
                    {item.badge !== undefined && item.badge > 0 && (
                      <span className="bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-[20px] text-center">
                        {item.badge > 99 ? '99+' : item.badge}
                      </span>
                    )}
                  </>
                )}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer da sidebar */}
      <div className="p-4 border-t border-slate-700 mt-auto">
        <button className="w-full flex items-center justify-center px-4 py-2 text-white bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors">
          <span className={`${isCollapsed ? '' : 'mr-2'} text-lg`}>↩️</span>
          {!isCollapsed && <span>Voltar ao Menu</span>}
        </button>
      </div>
    </aside>
  );
};

// Componente para ícones comuns
export const NavIcons = {
  Dashboard: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  ),
  Projects: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
    </svg>
  ),
  Actions: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
    </svg>
  ),
  Checklists: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  Reports: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  ),
  Settings: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  )
};

export default SideNav;
