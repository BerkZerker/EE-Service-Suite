import React from 'react';

type RadioOption = {
  value: string;
  label: string;
  description?: string;
};

interface RadioGroupProps {
  label?: string;
  name: string;
  options: RadioOption[];
  value: string;
  onChange: (value: string) => void;
  error?: string;
  className?: string;
  inline?: boolean;
}

export const RadioGroup: React.FC<RadioGroupProps> = ({
  label,
  name,
  options,
  value,
  onChange,
  error,
  className = '',
  inline = false,
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  // Generated ID for the group
  // This ID could be used for ARIA attributes if needed

  return (
    <div className={className}>
      {label && (
        // Use .form-label for theme-aware styling
        <label className="form-label mb-2">{label}</label>
      )}
      <div className={`space-y-2 ${inline ? 'flex flex-wrap gap-4 space-y-0' : ''}`}>
        {options.map((option) => (
          <div key={option.value} className={`flex items-start ${inline ? 'mr-4' : ''}`}>
            <div className="flex items-center h-5">
              <input
                id={`${name}-${option.value}`}
                name={name}
                type="radio"
                value={option.value}
                checked={value === option.value}
                onChange={handleChange}
                // Radio button theme styles: Light: gray border/bg. Dark: darker gray border/bg. Checked/Focus use primary color.
                className="h-4 w-4 text-primary-600 border-gray-300 focus:ring-primary-500 bg-white dark:bg-gray-700 dark:border-gray-600"
              />
            </div>
            <div className="ml-3 text-sm">
              {/* Option label theme styles */}
              <label htmlFor={`${name}-${option.value}`} className="font-medium text-gray-700 dark:text-gray-300">
                {option.label}
              </label>
              {option.description && (
                 // Option description theme styles
                <p className="text-gray-500 dark:text-gray-400">{option.description}</p>
              )}
            </div>
          </div>
        ))}
      </div>
      {/* Error styling is likely fine as is */}
      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default RadioGroup;
