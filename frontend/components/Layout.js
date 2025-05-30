import Navbar from './Navbar';
import Head from 'next/head';
import styles from '../styles/Layout.module.css'; // We'll create this CSS module next

export default function Layout({ children, title = "Yuri Oliveira - Portfolio" }) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <meta name="description" content="Yuri Oliveira's Professional Portfolio and Blog. Showcasing AI/ML, Python, Docker, FastAPI, and Next.js projects." />
        <link rel="icon" href="/favicon.ico" /> {/* Assuming favicon.ico will be in public folder */}
      </Head>
      <div className={styles.pageContainer}>
        <Navbar />
        <main className={styles.mainContent}>
          {children}
        </main>
        <footer className={styles.footer}>
          <p>&copy; {new Date().getFullYear()} Yuri Oliveira. All rights reserved.</p>
          {/* Add social links or other footer content here if desired */}
        </footer>
      </div>
    </>
  );
}
