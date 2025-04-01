import { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAuth } from '../contexts/auth-context';
import ThemeToggle from '../components/ui/ThemeToggle'; // Import ThemeToggle
import Button from '../components/ui/Button'; // Import Button component

// Form validation schema
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

const Login = () => {
  const { login, isAuthenticated, loading, error } = useAuth();
  const navigate = useNavigate();
  const [submitError, setSubmitError] = useState<string | null>(null);
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting } 
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setSubmitError(null);
    try {
      await login(data.email, data.password);
      navigate('/');
    } catch (err: any) {
      setSubmitError(err.message || 'Login failed');
    }
  };

  // Redirect if already authenticated
  if (isAuthenticated && !loading) {
    return <Navigate to="/" />;
  }

  return (
    // Use theme background
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-background)] relative p-4">
       {/* Add Theme Toggle Button to top right */}
       <div className="absolute top-4 right-4">
         <ThemeToggle />
       </div>

      {/* Use card class for consistent styling */}
      <div className="card max-w-md w-full p-8 space-y-8"> {/* Removed hardcoded bg/shadow */}
        <div className="text-center">
           {/* Use theme text color */}
          <h1 className="text-2xl font-bold text-[var(--color-text)]">EE Service Suite</h1>
           {/* Use theme text color with opacity */}
          <p className="mt-2 text-[var(--color-text)] opacity-75">Sign in to your account</p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {(error || submitError) && (
             // Keep error styling specific for now
            <div className="bg-red-900/50 text-red-200 p-3 rounded">
              {error || submitError}
            </div>
          )}
          
          <div>
             {/* Use form-label class */}
            <label htmlFor="email" className="form-label">
              Email
            </label>
            <div className="mt-1">
              {/* Use form-input class */}
              <input
                id="email"
                type="email"
                autoComplete="email"
                className={`form-input ${errors.email ? 'border-red-500' : 'border-[var(--color-border)]'}`} // Add error border conditionally
                {...register('email')}
              />
              {errors.email && (
                 // Use form-error class
                <p className="form-error">{errors.email.message}</p>
              )}
            </div>
          </div>

          <div>
             {/* Use form-label class */}
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <div className="mt-1">
               {/* Use form-input class */}
              <input
                id="password"
                type="password"
                autoComplete="current-password"
                className={`form-input ${errors.password ? 'border-red-500' : 'border-[var(--color-border)]'}`} // Add error border conditionally
                {...register('password')}
              />
              {errors.password && (
                 // Use form-error class
                <p className="form-error">{errors.password.message}</p>
              )}
            </div>
          </div>

          <div>
             {/* Use Button component */}
            <Button
              type="submit"
              variant="primary" // Use primary (orange) button
              isLoading={isSubmitting}
              className="w-full"
            >
              {isSubmitting ? 'Signing in...' : 'Sign in'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
