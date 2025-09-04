import React from 'react';
import { colors } from '../../tokens/colors';

interface TopBarProps {
  title?: string;
  user?: {
    name: string;
    email: string;
    avatar?: string;
  };
  onThemeToggle?: () => void;
  onUserMenuClick?: () => void;
  showThemeToggle?: boolean;
  showUserMenu?: boolean;
  className?: string;
}

export const TopBar: React.FC<TopBarProps> = ({
  title = "Dashboard Central",
  user,
  onThemeToggle,
  onUserMenuClick,
  showThemeToggle = true,
  showUserMenu = true,
  className = ""
}) => {
  return (
    <header className={`bg-slate-900 border-b border-slate-700 px-6 py-4 ${className}`}>
      <div className="flex items-center justify-between">
        {/* Logo e Título */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-3">
            <img 
              src="data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3e%3crect width='100' height='100' rx='20' fill='%230761FF'/%3e%3ctext x='50' y='55' font-family='Inter, sans-serif' font-size='75' font-weight='bold' fill='white' text-anchor='middle' dominant-baseline='middle'%3eB%3c/text%3e%3c/svg%3e" 
              alt="Betha Logo" 
              className="w-10 h-10 rounded-lg"
            />
            <div>
              <h1 className="text-xl font-bold text-white">{title}</h1>
              <p className="text-sm text-slate-400">Betha Sistemas</p>
            </div>
          </div>
        </div>

        {/* Ações do usuário */}
        <div className="flex items-center space-x-4">
          {/* Toggle de tema */}
          {showThemeToggle && (
            <button
              onClick={onThemeToggle}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
              aria-label="Alternar tema"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>
          )}

          {/* Link para documentação */}
          <a
            href="/docs"
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
            aria-label="Documentação"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </a>

          {/* Menu do usuário */}
          {showUserMenu && user && (
            <div className="relative">
              <button
                onClick={onUserMenuClick}
                className="flex items-center space-x-3 p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
                aria-label="Menu do usuário"
              >
                {user.avatar ? (
                  <img
                    src={user.avatar}
                    alt={user.name}
                    className="w-8 h-8 rounded-full"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
                    <span className="text-sm font-medium text-white">
                      {user.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                )}
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-white">{user.name}</p>
                  <p className="text-xs text-slate-400">{user.email}</p>
                </div>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default TopBar;
