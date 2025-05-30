import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';
import Head from 'next/head';
import styles from '../styles/Profile.module.css'; // Create this CSS module

// Set page title
Profile.title = "My Profile | Yuri Oliveira";

export default function Profile() {
  const { user, isLoading, isAuthenticated, error } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login'); // Redirect to login if not authenticated and not loading
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return <div className={styles.loading}>Loading profile...</div>;
  }

  if (!isAuthenticated) {
    // This state might be brief due to the redirect, or if redirect hasn't happened yet
    return <div className={styles.loading}>Redirecting to login...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error loading profile: {error}</div>;
  }

  if (!user) {
    // Should be covered by isLoading or !isAuthenticated, but as a fallback
    return <div className={styles.loading}>No user data found. You may need to re-login.</div>;
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>{Profile.title}</title>
        <meta name="description" content="User profile page for YuriODev Platform." />
      </Head>

      <header className={styles.header}>
        <h1>My Profile</h1>
      </header>

      <section className={`card ${styles.profileDetails}`}> {/* Using global .card style */}
        <h2>Account Information</h2>
        <div className={styles.detailItem}>
          <strong>Full Name:</strong> <span>{user.full_name || 'Not provided'}</span>
        </div>
        <div className={styles.detailItem}>
          <strong>Email:</strong> <span>{user.email}</span>
        </div>
        <div className={styles.detailItem}>
          <strong>Login Provider:</strong> <span className={styles.provider}>{user.provider || 'N/A'}</span>
        </div>
        <div className={styles.detailItem}>
          <strong>User ID:</strong> <span>{user.id}</span>
        </div>
        <div className={styles.detailItem}>
          <strong>Active:</strong> <span>{user.is_active ? 'Yes' : 'No'}</span>
        </div>
        <div className={styles.detailItem}>
          <strong>Superuser:</strong> <span>{user.is_superuser ? 'Yes' : 'No'}</span>
        </div>
        <div className={styles.detailItem}>
          <strong>Joined:</strong> <span>{new Date(user.created_at).toLocaleDateString()}</span>
        </div>
         {/* Add more user details here as needed */}
      </section>

      {/* Placeholder for future profile actions e.g. edit profile, change password (if applicable) */}
      {/*
      <section className={styles.profileActions}>
        <h2>Actions</h2>
        <button className="button button-secondary">Edit Profile</button>
      </section>
      */}
    </div>
  );
}
