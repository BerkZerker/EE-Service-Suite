import React, { forwardRef, InputHTMLAttributes } from 'react';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  className?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      className = '',
      id,
      ...props
    },
    ref
  ) => {
    // Generate a unique ID if one isn't provided
    const inputId = id || `input-${Math.random().toString(36).substring(2, 9)}`;

    return (
      <div className={className}>
        {label && (
          // Use .form-label for theme-aware styling
          <label htmlFor={inputId} className="form-label">
            {label}
          </label>
        )}
        <div className="relative"> {/* Removed rounded-md shadow-sm, handled by .form-input */}
          {leftIcon && (
            // Adjust icon color for theme
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 dark:text-gray-500">
              {leftIcon}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            // Apply .form-input class and handle padding for icons
            // Error border is handled within .form-input logic (implicitly via focus ring potentially, or could add specific error class if needed)
            className={`
              form-input 
              ${leftIcon ? 'pl-10' : ''} 
              ${rightIcon ? 'pr-10' : ''} 
              ${error ? 'border-red-500 focus:ring-red-500' : ''} {/* Add specific error border/focus */}
            `}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={helperText || error ? `${inputId}-description` : undefined}
            {...props}
          />
          {rightIcon && (
             // Adjust icon color for theme
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-gray-400 dark:text-gray-500">
              {rightIcon}
            </div>
          )}
        </div>
        {(helperText || error) && (
          // Use .form-error or .form-helper for theme-aware styling
          <p
            id={`${inputId}-description`}
            className={error ? 'form-error' : 'form-helper'}
          >
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
