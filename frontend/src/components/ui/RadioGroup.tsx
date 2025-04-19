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
                // Use theme variables for border and background, keep primary for checked/focus
                className="h-4 w-4 text-[var(--color-primary)] border-[var(--color-border)] focus:ring-[var(--color-primary)] bg-[var(--color-background)] focus:ring-offset-0 focus:ring-2" // Added focus:ring-2 and offset-0 for better visibility
              />
            </div>
            <div className="ml-3 text-sm">
              {/* Use theme variable for label text */}
              <label htmlFor={`${name}-${option.value}`} className="font-medium text-[var(--color-text)]">
                {option.label}
              </label>
              {option.description && (
                 // Use theme variable (secondary) for description text
                <p className="text-[var(--color-secondary)]">{option.description}</p>
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
