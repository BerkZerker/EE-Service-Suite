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
  // Note: Dark mode styles added/adjusted to align with index.css where applicable
  switch (variant) {
    case 'primary':
      // Use primary (blue) for both light and dark modes
      return 'bg-primary-600 hover:bg-primary-700 text-white'; // Primary is blue in both modes
    case 'secondary':
      // Use secondary for light, blue outline for dark
      return 'bg-secondary-600 hover:bg-secondary-700 text-white dark:bg-transparent dark:border dark:border-primary-500 dark:text-primary-500 dark:hover:bg-primary-900/20';
    case 'danger':
      // Danger colors consistent across themes
      return 'bg-red-600 hover:bg-red-700 text-white';
    case 'success':
      return 'bg-green-600 hover:bg-green-700 text-white';
    case 'warning':
      // Warning colors consistent
      return 'bg-yellow-500 hover:bg-yellow-600 text-black';
    case 'outline':
      // Explicit light/dark variants using gray for dark background
      return 'bg-transparent border border-gray-300 hover:bg-gray-100 text-gray-700 dark:border-gray-600 dark:hover:bg-gray-700 dark:text-gray-300';
    case 'ghost':
      // Explicit light/dark variants using gray for dark background
      return 'bg-transparent hover:bg-gray-100 text-gray-700 dark:hover:bg-gray-700 dark:text-gray-300';
    case 'subtle':
       // Explicit light/dark variants using gray for dark background
      return 'bg-gray-100 hover:bg-gray-200 text-gray-800 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-300';
    default: // Default to primary styling (blue)
      return 'bg-primary-600 hover:bg-primary-700 text-white'; // Removed dark overrides
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
        // Use primary-500 for focus ring in both light and dark modes
        className={`inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:focus:ring-primary-500 dark:focus:ring-offset-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${variantClasses} ${sizeClasses} ${className}`}
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
