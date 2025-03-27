import React from 'react';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  className?: string;
  headerAction?: React.ReactNode;
  footer?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  children,
  title,
  className = '',
  headerAction,
  footer,
}) => {
  return (
    <div className={`bg-gray-800 rounded-lg shadow-md overflow-hidden ${className}`}>
      {(title || headerAction) && (
        <div className="px-4 py-3 bg-gray-800 border-b border-gray-700 flex justify-between items-center">
          {title && <h3 className="text-lg font-medium text-white">{title}</h3>}
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}
      <div className="p-4">{children}</div>
      {footer && (
        <div className="px-4 py-3 bg-gray-700 border-t border-gray-600">{footer}</div>
      )}
    </div>
  );
};

export default Card;