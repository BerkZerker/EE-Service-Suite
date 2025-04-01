import React from 'react';

interface SpinnerProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'primary' | 'secondary' | 'white';
  className?: string;
}

const getSizeClasses = (size: SpinnerProps['size']): string => {
  switch (size) {
    case 'xs':
      return 'h-3 w-3';
    case 'sm':
      return 'h-4 w-4';
    case 'md':
      return 'h-6 w-6';
    case 'lg':
      return 'h-8 w-8';
    case 'xl':
      return 'h-12 w-12';
    default:
      return 'h-6 w-6';
  }
};

const getVariantClasses = (variant: SpinnerProps['variant']): string => {
  switch (variant) {
    case 'primary':
      // Use CSS variable for primary color
      return 'text-[var(--color-primary)]';
    case 'secondary':
       // Use CSS variable for secondary color
      return 'text-[var(--color-secondary)]';
    case 'white':
      // Keep white as an option if needed for specific contexts
      return 'text-white';
    default:
       // Default to primary color using CSS variable
      return 'text-[var(--color-primary)]';
  }
};

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  variant = 'primary',
  className = '',
}) => {
  const sizeClasses = getSizeClasses(size);
  const variantClasses = getVariantClasses(variant);

  return (
    <svg
      className={`animate-spin ${sizeClasses} ${variantClasses} ${className}`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  );
};

export default Spinner;
