import React, { SelectHTMLAttributes, forwardRef } from 'react';

export interface SelectOption {
  value: string | number;
  label: string;
}

export interface SelectProps extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'onChange'> {
  options: SelectOption[];
  label?: string;
  error?: string;
  helperText?: string;
  className?: string;
  onChange?: (value: string) => void;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      label,
      options,
      error,
      helperText,
      className = '',
      id,
      onChange,
      ...props
    },
    ref
  ) => {
    // Generate a unique ID if one isn't provided
    const selectId = id || `select-${Math.random().toString(36).substring(2, 9)}`;

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
      if (onChange) {
        onChange(e.target.value);
      }
    };

    return (
      <div className={className}>
        {label && (
          // Use .form-label for theme-aware styling
          <label htmlFor={selectId} className="form-label">
            {label}
          </label>
        )}
        {/* Removed relative rounded-md shadow-sm, handled by .form-input */}
        <div className="relative"> 
          <select
            ref={ref}
            id={selectId}
            // Apply .form-input class and keep appearance-none
            // Error border is handled within .form-input logic or added explicitly
            className={`
              form-input 
              pr-10 {/* Keep padding for arrow */}
              appearance-none
              ${error ? 'border-red-500 focus:ring-red-500' : ''} {/* Add specific error border/focus */}
            `}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={helperText || error ? `${selectId}-description` : undefined}
            onChange={handleChange}
            {...props}
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
            {/* Option styles might need adjustment if they don't inherit correctly, but usually browser default is fine */}
          </select>
          {/* Adjust arrow color for theme */}
          <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none text-gray-400 dark:text-gray-500">
            <svg
              className="h-5 w-5" // Removed text-gray-400, color comes from parent div
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </div>
        </div>
        {(helperText || error) && (
          // Use .form-error or .form-helper for theme-aware styling
          <p
            id={`${selectId}-description`}
            className={error ? 'form-error' : 'form-helper'}
          >
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

Select.displayName = 'Select';

export default Select;
