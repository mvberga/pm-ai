import React from 'react';

interface BreadcrumbItem {
  label: string;
  href?: string;
  isActive?: boolean;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  onItemClick?: (item: BreadcrumbItem, index: number) => void;
  className?: string;
  separator?: React.ReactNode;
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  onItemClick,
  className = "",
  separator
}) => {
  const defaultSeparator = (
    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  );

  const handleItemClick = (item: BreadcrumbItem, index: number) => {
    if (onItemClick && !item.isActive) {
      onItemClick(item, index);
    }
  };

  if (items.length === 0) {
    return null;
  }

  return (
    <nav className={`flex items-center space-x-2 text-sm ${className}`} aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        {items.map((item, index) => (
          <li key={index} className="flex items-center">
            {index > 0 && (
              <span className="mx-2">
                {separator || defaultSeparator}
              </span>
            )}
            
            {item.isActive ? (
              <span className="text-primary-400 font-medium" aria-current="page">
                {item.label}
              </span>
            ) : item.href ? (
              <a
                href={item.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleItemClick(item, index);
                }}
                className="text-slate-300 hover:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
              >
                {item.label}
              </a>
            ) : (
              <button
                onClick={() => handleItemClick(item, index)}
                className="text-slate-300 hover:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
              >
                {item.label}
              </button>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};

// Hook para gerenciar breadcrumbs
export const useBreadcrumbs = (initialItems: BreadcrumbItem[] = []) => {
  const [items, setBreadcrumbItems] = React.useState<BreadcrumbItem[]>(initialItems);

  const addItem = (item: BreadcrumbItem) => {
    setBreadcrumbItems(prev => [...prev, item]);
  };

  const removeItem = (index: number) => {
    setBreadcrumbItems(prev => prev.slice(0, index + 1));
  };

  const updateItem = (index: number, item: BreadcrumbItem) => {
    setBreadcrumbItems(prev => prev.map((existingItem, i) => 
      i === index ? item : existingItem
    ));
  };

  const setItems = (newItems: BreadcrumbItem[]) => {
    setBreadcrumbItems(newItems);
  };

  const clear = () => {
    setBreadcrumbItems([]);
  };

  return {
    items,
    addItem,
    removeItem,
    updateItem,
    setItems,
    clear
  };
};

export default Breadcrumbs;
