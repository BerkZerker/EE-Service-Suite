import React from 'react';
import { FiSun, FiMoon } from 'react-icons/fi'; // Import icons
import { useTheme } from '../../contexts/ThemeContext'; // Import useTheme hook
import Button from './Button'; // Assuming a Button component exists for consistent styling

const ThemeToggle: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <Button
      onClick={toggleTheme}
      variant="outline" // Use outline variant for less emphasis
      size="sm" // Smaller size might fit better in a header
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      className="p-2" // Adjust padding if needed for icon-only button
    >
      {theme === 'light' ? (
        <FiMoon className="w-5 h-5" /> // Show moon in light mode
      ) : (
        <FiSun className="w-5 h-5" /> // Show sun in dark mode
      )}
    </Button>
  );
};

export default ThemeToggle;
