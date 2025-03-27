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
      {title && <h3 className="text-lg font-medium text-white mb-2">{title}</h3>}
      {description && <p className="text-sm text-gray-400 mb-4">{description}</p>}
      <div className="space-y-4">{children}</div>
    </div>
  );
};

export default FormGroup;