import Link from 'next/link';
import styles from '../styles/Navbar.module.css';
import { useAuth } from '../contexts/AuthContext'; // Import useAuth

export default function Navbar() {
  const { user, isLoading, logout, isAuthenticated } = useAuth(); // Get auth state and functions

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Link href="/">Yuri Oliveira</Link>
      </div>
      <ul className={styles.navLinks}>
        <li>
          <Link href="/">Home</Link>
        </li>
        <li>
          <Link href="/skills">Skills</Link>
        </li>
        <li>
          <Link href="/projects">Projects</Link>
        </li>
        <li>
          <Link href="/courses">Courses</Link> {/* New Courses Link */}
        </li>
        <li>
          <Link href="/blog">Blog</Link>
        </li>
        {/* Authentication Links */}
        {isLoading ? (
          <li className={styles.loadingNavItem}>Loading...</li>
        ) : isAuthenticated ? (
          <>
            <li>
              <Link href="/profile">Profile</Link>
            </li>
            <li>
              <button onClick={logout} className={styles.logoutButton}>Logout</button>
            </li>
          </>
        ) : (
          <li>
            <Link href="/login">Login</Link>
          </li>
        )}
        {/* Future links:
        <li>
          <Link href="/contact">Contact</Link>
        </li>
        */}
      </ul>
    </nav>
  );
}
