import React, { InputHTMLAttributes, forwardRef } from 'react';

export interface DatePickerProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type' | 'onChange'> {
  label?: string;
  error?: string;
  helperText?: string;
  className?: string;
  onChange?: (value: string) => void;
}

export const DatePicker = forwardRef<HTMLInputElement, DatePickerProps>(
  (
    {
      label,
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
    const datePickerId = id || `datepicker-${Math.random().toString(36).substring(2, 9)}`;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (onChange) {
        onChange(e.target.value);
      }
    };

    return (
      <div className={className}>
        {label && (
          // Use .form-label for theme-aware styling
          <label htmlFor={datePickerId} className="form-label">
            {label}
          </label>
        )}
        {/* Removed relative rounded-md shadow-sm, handled by .form-input */}
        <div className="relative"> 
          <input
            ref={ref}
            id={datePickerId}
            type="date"
            // Apply .form-input class
            // Error border is handled within .form-input logic or added explicitly
            // Note: Date picker icon styling might be browser-dependent
            className={`
              form-input
              ${error ? 'border-red-500 focus:ring-red-500' : ''} {/* Add specific error border/focus */}
            `}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={helperText || error ? `${datePickerId}-description` : undefined}
            onChange={handleChange}
            {...props}
          />
        </div>
        {(helperText || error) && (
          // Use .form-error or .form-helper for theme-aware styling
          <p
            id={`${datePickerId}-description`}
            className={error ? 'form-error' : 'form-helper'}
          >
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

DatePicker.displayName = 'DatePicker';

export default DatePicker;
