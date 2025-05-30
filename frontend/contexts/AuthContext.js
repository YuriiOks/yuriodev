import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Start with loading true for initial fetch
  const [error, setError] = useState(null);
  const router = useRouter();

  // Use NEXT_PUBLIC_API_BASE_URL as defined in .env.local and docker-compose.yml
  // This URL should point directly to the API's v1 root.
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

  const fetchUser = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/users/me`, { // Path relative to API_BASE_URL
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Cookies are sent automatically by the browser, no need to set Authorization header here
        },
      });
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else if (response.status === 401 || response.status === 403) {
        setUser(null); // Not authenticated or not authorized
        // Don't set error for 401/403 as it's an expected state for non-logged-in users
      } else {
        // Handle other errors (e.g., server error)
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to fetch user data.');
        setUser(null);
      }
    } catch (err) {
      setError('An error occurred while fetching user data. Is the backend running?');
      setUser(null);
      console.error("fetchUser error:", err);
    } finally {
      setIsLoading(false);
    }
  }, [API_BASE_URL]);

  // Initial user fetch on component mount
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const loginWithProvider = (providerName) => {
    setIsLoading(true);
    // Redirects to backend which then redirects to OAuth provider
    // The backend login URL is relative to API_BASE_URL
    window.location.href = `${API_BASE_URL}/auth/login/${providerName}`;
  };

  const logout = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/auth/logout`, { // Path relative to API_BASE_URL
        method: 'POST',
      });
      if (response.ok) {
        setUser(null);
        // Redirect to home or login page after logout
        // Ensure cookie is cleared by backend. Frontend just updates state.
        router.push('/');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Logout failed.');
      }
    } catch (err) {
      setError('An error occurred during logout.');
      console.error("logout error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, error, loginWithProvider, logout, fetchUser, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
