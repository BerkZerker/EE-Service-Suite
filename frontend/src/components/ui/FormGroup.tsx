import React from 'react';

interface FormGroupProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  className?: string;
}

export const FormGroup: React.FC<FormGroupProps> = ({
  children,
  title,
  description,
  className = '',
}) => {
  return (
    <div className={`mb-6 ${className}`}>
      {/* Title text color for light/dark */}
      {title && <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">{title}</h3>}
      {/* Description text color for light/dark */}
      {description && <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{description}</p>}
      <div className="space-y-4">{children}</div>
    </div>
  );
};

export default FormGroup;
