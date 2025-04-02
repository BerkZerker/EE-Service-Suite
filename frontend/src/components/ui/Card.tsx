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
        // Header: Use theme variables - Background matches card body, theme border, theme text
        <div className="px-4 py-3 bg-[var(--color-background)] border-b border-[var(--color-border)] flex justify-between items-center">
          {/* Title text color uses theme text color */}
          {title && <h3 className="text-lg font-medium text-[var(--color-text)]">{title}</h3>}
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}
      {/* Main content padding */}
      <div className="p-4">{children}</div>
      {footer && (
         // Footer: Use theme variables - Accent background, theme border
        <div className="px-4 py-3 bg-[var(--color-accent)] bg-opacity-20 border-t border-[var(--color-border)]">{footer}</div> // Using accent with opacity for footer
      )}
    </div>
  );
};

export default Card;
