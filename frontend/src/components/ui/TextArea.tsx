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
          <label htmlFor={textAreaId} className="block text-sm font-medium text-gray-300 mb-1">
            {label}
          </label>
        )}
        <div className="relative rounded-md shadow-sm">
          <textarea
            ref={ref}
            id={textAreaId}
            rows={rows}
            className={`
              w-full rounded-md shadow-sm 
              px-3 py-2 bg-gray-700 border 
              ${error ? 'border-red-500' : 'border-gray-600'} 
              text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
            `}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={helperText || error ? `${textAreaId}-description` : undefined}
            {...props}
          />
        </div>
        {(helperText || error) && (
          <p
            id={`${textAreaId}-description`}
            className={`mt-1 text-sm ${error ? 'text-red-500' : 'text-gray-400'}`}
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