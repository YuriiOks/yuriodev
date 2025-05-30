import Link from 'next/link';
import styles from '../styles/Navbar.module.css'; // We'll create this CSS module next

export default function Navbar() {
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
          <Link href="/blog">Blog</Link>
        </li>
        {/* Future links:
        <li>
          <Link href="/contact">Contact</Link>
        </li>
        */}
      </ul>
    </nav>
  );
}
