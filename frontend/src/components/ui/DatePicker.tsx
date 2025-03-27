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
          <label htmlFor={datePickerId} className="block text-sm font-medium text-gray-300 mb-1">
            {label}
          </label>
        )}
        <div className="relative rounded-md shadow-sm">
          <input
            ref={ref}
            id={datePickerId}
            type="date"
            className={`
              w-full rounded-md shadow-sm 
              px-3 py-2 bg-gray-700 border 
              ${error ? 'border-red-500' : 'border-gray-600'} 
              text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
            `}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={helperText || error ? `${datePickerId}-description` : undefined}
            onChange={handleChange}
            {...props}
          />
        </div>
        {(helperText || error) && (
          <p
            id={`${datePickerId}-description`}
            className={`mt-1 text-sm ${error ? 'text-red-500' : 'text-gray-400'}`}
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