import React, { ButtonHTMLAttributes } from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'outline' | 'ghost' | 'subtle';
type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  className?: string;
}

const getVariantClasses = (variant: ButtonVariant): string => {
  // Return global CSS class names defined in index.css
  // These classes already use the CSS variables for theming.
  switch (variant) {
    case 'primary':
      return 'btn-primary'; // Uses --color-primary (orange)
    case 'secondary':
      return 'btn-secondary'; // Uses --color-secondary (slate blue)
    case 'danger':
      // Keep specific Tailwind classes for danger as no theme color was provided
      return 'bg-red-600 hover:bg-red-700 text-white';
    case 'success':
      // Keep specific Tailwind classes for success
      return 'bg-green-600 hover:bg-green-700 text-white';
    case 'warning':
      // Keep specific Tailwind classes for warning
      return 'bg-yellow-500 hover:bg-yellow-600 text-black';
    case 'outline':
      return 'btn-outline'; // Uses --color-border, --color-accent, etc.
    case 'ghost':
      // Map ghost to outline for now
      return 'btn-outline border-transparent hover:border-[var(--color-border)]'; // Make border transparent initially
    case 'subtle':
      // Map subtle to outline with slightly different hover
       return 'btn-outline border-transparent bg-opacity-10 hover:bg-opacity-20'; // Use background opacity
    default: // Default to primary styling
      return 'btn-primary';
  }
};

const getSizeClasses = (size: ButtonSize): string => {
  switch (size) {
    case 'xs':
      return 'px-2 py-1 text-xs';
    case 'sm':
      return 'px-3 py-1.5 text-sm';
    case 'md':
      return 'px-4 py-2 text-sm';
    case 'lg':
      return 'px-5 py-2.5 text-base';
    case 'xl':
      return 'px-6 py-3 text-lg';
    default:
      return 'px-4 py-2 text-sm';
  }
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      className = '',
      disabled,
      ...props
    },
    ref
  ) => {
    const variantClasses = getVariantClasses(variant);
    const sizeClasses = getSizeClasses(size);

    return (
      <button
        ref={ref}
        // Use CSS variable for focus ring color
        className={`inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--color-primary)] dark:focus:ring-offset-[var(--color-background)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${variantClasses} ${sizeClasses} ${className}`}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <svg className="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        )}
        {!isLoading && leftIcon && <span className="mr-2">{leftIcon}</span>}
        {children}
        {!isLoading && rightIcon && <span className="ml-2">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
