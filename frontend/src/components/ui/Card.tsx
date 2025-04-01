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
  // Apply the .card class from index.css for base styling (light/dark)
  // Keep overflow-hidden and allow additional classes via `className`
  return (
    <div className={`card overflow-hidden ${className}`}>
      {(title || headerAction) && (
        // Header: Light: lighter gray bg, gray border. Dark: slightly lighter dark bg, darker gray border
        <div className="px-4 py-3 bg-gray-50 border-b border-gray-200 flex justify-between items-center dark:bg-gray-700/50 dark:border-gray-700">
          {/* Title text color should inherit from .card */}
          {title && <h3 className="text-lg font-medium">{title}</h3>}
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}
      {/* Main content padding */}
      <div className="p-4">{children}</div>
      {footer && (
         // Footer: Light: lighter gray bg, gray border. Dark: slightly lighter dark bg, darker gray border
        <div className="px-4 py-3 bg-gray-50 border-t border-gray-200 dark:bg-gray-700/50 dark:border-gray-700">{footer}</div>
      )}
    </div>
  );
};

export default Card;
