import React from 'react';
import { colors, getStatusColor } from '../../tokens/colors';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
    label?: string;
  };
  status?: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  loading?: boolean;
  onClick?: () => void;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  status = 'neutral',
  loading = false,
  onClick,
  className = "",
  size = 'md'
}) => {
  const getStatusStyles = () => {
    switch (status) {
      case 'success':
        return {
          bg: 'bg-green-900/20',
          border: 'border-green-500/20',
          text: 'text-green-400',
          icon: 'text-green-500'
        };
      case 'warning':
        return {
          bg: 'bg-yellow-900/20',
          border: 'border-yellow-500/20',
          text: 'text-yellow-400',
          icon: 'text-yellow-500'
        };
      case 'error':
        return {
          bg: 'bg-red-900/20',
          border: 'border-red-500/20',
          text: 'text-red-400',
          icon: 'text-red-500'
        };
      case 'info':
        return {
          bg: 'bg-blue-900/20',
          border: 'border-blue-500/20',
          text: 'text-blue-400',
          icon: 'text-blue-500'
        };
      default:
        return {
          bg: 'bg-slate-800',
          border: 'border-slate-700',
          text: 'text-slate-200',
          icon: 'text-slate-400'
        };
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'sm':
        return {
          container: 'p-4',
          title: 'text-sm',
          value: 'text-xl',
          subtitle: 'text-xs'
        };
      case 'lg':
        return {
          container: 'p-8',
          title: 'text-lg',
          value: 'text-4xl',
          subtitle: 'text-base'
        };
      default:
        return {
          container: 'p-6',
          title: 'text-base',
          value: 'text-2xl',
          subtitle: 'text-sm'
        };
    }
  };

  const statusStyles = getStatusStyles();
  const sizeStyles = getSizeStyles();

  if (loading) {
    return (
      <div className={`bg-slate-800 rounded-lg shadow-sm border border-slate-700 ${sizeStyles.container} ${className}`}>
        <div className="animate-pulse">
          <div className="h-4 bg-slate-700 rounded w-3/4 mb-2"></div>
          <div className="h-8 bg-slate-700 rounded w-1/2 mb-2"></div>
          <div className="h-3 bg-slate-700 rounded w-1/3"></div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className={`
        ${statusStyles.bg} ${statusStyles.border} 
        rounded-lg shadow-sm border 
        ${sizeStyles.container} 
        ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}
        ${className}
      `}
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className={`font-semibold text-slate-400 ${sizeStyles.title} mb-2`}>
            {title}
          </h3>
          
          <p className={`font-bold ${statusStyles.text} ${sizeStyles.value} mb-1`}>
            {typeof value === 'number' ? value.toLocaleString('pt-BR') : value}
          </p>
          
          {subtitle && (
            <p className={`text-slate-400 ${sizeStyles.subtitle}`}>
              {subtitle}
            </p>
          )}
          
          {trend && (
            <div className="flex items-center mt-2">
              <span className={`text-xs ${trend.isPositive ? 'text-green-400' : 'text-red-400'}`}>
                {trend.isPositive ? '↗' : '↘'} {Math.abs(trend.value)}%
              </span>
              {trend.label && (
                <span className="text-xs text-slate-500 ml-2">
                  {trend.label}
                </span>
              )}
            </div>
          )}
        </div>
        
        {icon && (
          <div className={`${statusStyles.icon} ml-4`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
};

// Componentes de ícones comuns para KPIs
export const KPIIcons = {
  Projects: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
    </svg>
  ),
  Actions: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
    </svg>
  ),
  Money: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
    </svg>
  ),
  Users: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
    </svg>
  ),
  Clock: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  CheckCircle: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  Alert: (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
    </svg>
  )
};

export default KPICard;
