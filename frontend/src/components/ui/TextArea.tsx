import { TextareaHTMLAttributes, forwardRef } from 'react';

export interface TextAreaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  className?: string;
  rows?: number;
}

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(
  (
    {
      label,
      error,
      helperText,
      className = '',
      id,
      rows = 3,
      ...props
    },
    ref
  ) => {
    // Generate a unique ID if one isn't provided
    const textAreaId = id || `textarea-${Math.random().toString(36).substring(2, 9)}`;

    return (
      <div className={className}>
        {label && (
          // Use .form-label for theme-aware styling
          <label htmlFor={textAreaId} className="form-label">
            {label}
          </label>
        )}
        {/* Removed relative rounded-md shadow-sm, handled by .form-input */}
        <div className="relative"> 
          <textarea
            ref={ref}
            id={textAreaId}
            rows={rows}
            // Apply .form-input class
            // Error border is handled within .form-input logic or added explicitly
            className={`
              form-input
              ${error ? 'border-red-500 focus:ring-red-500' : ''} {/* Add specific error border/focus */}
            `}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={helperText || error ? `${textAreaId}-description` : undefined}
            {...props}
          />
        </div>
        {(helperText || error) && (
          // Use .form-error or .form-helper for theme-aware styling
          <p
            id={`${textAreaId}-description`}
            className={error ? 'form-error' : 'form-helper'}
          >
            {error || helperText}
          </p>
        )}
      </div>
    );
  }
);

TextArea.displayName = 'TextArea';

export default TextArea;
