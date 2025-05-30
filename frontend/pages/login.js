import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import Head from 'next/head';
import styles from '../styles/Login.module.css'; // Create this CSS module

// Set page title
Login.title = "Login | Yuri Oliveira";

export default function Login() {
  const { user, loginWithProvider, isLoading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      router.push('/profile'); // Redirect to profile if already logged in
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  // If user becomes authenticated during render (e.g. after silent refresh), this will also redirect
  if (isAuthenticated) {
    return <div className={styles.loading}>Redirecting...</div>;
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>{Login.title}</title>
        <meta name="description" content="Login to YuriODev Platform" />
      </Head>
      <div className={styles.loginBox}>
        <h1>Login</h1>
        <p>Choose your preferred provider to continue.</p>
        <div className={styles.buttonGroup}>
          <button
            onClick={() => loginWithProvider('google')}
            className={`${styles.button} ${styles.googleButton}`}
            disabled={isLoading}
          >
            <span className={styles.iconWrapper}>
              {/* Placeholder for Google icon, you can use an SVG or an icon library */}
              <svg className={styles.icon} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M22.56,12.25C22.56,11.47 22.49,10.72 22.36,10H12V14.26H17.94C17.64,15.93 16.73,17.31 15.22,18.25V21.09H19.16C21.32,19.13 22.56,16.05 22.56,12.25Z" fill="#4285F4"/><path d="M12,23C14.97,23 17.46,22.04 19.16,20.09L15.22,17.25C14.21,17.95 13.08,18.36 12,18.36C9.48,18.36 7.3,16.63 6.39,14.26H2.34V17.1C4.04,20.53 7.79,23 12,23Z" fill="#34A853"/><path d="M6.39,13.26C6.14,12.55 6,11.79 6,11C6,10.21 6.14,9.45 6.39,8.74V5.9H2.34C1.49,7.58 1,9.22 1,11C1,12.78 1.49,14.42 2.34,16.1L6.39,13.26Z" fill="#FBBC05"/><path d="M12,5.64C13.47,5.64 14.73,6.15 15.69,7.06L19.25,3.5C17.46,1.79 14.97,1 12,1C7.79,1 4.04,3.47 2.34,6.9L6.39,9.74C7.3,7.37 9.48,5.64 12,5.64Z" fill="#EA4335"/></svg>
            </span>
            Login with Google
          </button>
          <button
            onClick={() => loginWithProvider('github')}
            className={`${styles.button} ${styles.githubButton}`}
            disabled={isLoading}
          >
             <span className={styles.iconWrapper}>
              {/* Placeholder for GitHub icon */}
              <svg className={styles.icon} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
            </span>
            Login with GitHub
          </button>
        </div>
      </div>
    </div>
  );
}
