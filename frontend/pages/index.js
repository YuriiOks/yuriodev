import Head from 'next/head';
import styles from '../styles/Home.module.css'; // Page-specific styles
import Link from 'next/link';
import WaitlistForm from '../components/WaitlistForm'; // Import the new component

// This is for setting the page title in _app.js
Home.title = "Home | Yuri Oliveira";

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        {/* Specific meta tags for this page, if needed, supplementing Layout's Head */}
        <meta name="description" content="Welcome to the portfolio of Yuri Oliveira, a software developer specializing in AI/ML, Python, and modern web technologies." />
      </Head>

      <header className={styles.header}>
        <h1>Hello, I'm Yuri Oliveira</h1>
        <p className={styles.subtitle}>Software Developer | AI & Machine Learning Enthusiast | Lifelong Learner</p>
      </header>

      <section className={styles.bioSection}>
        <h2>About Me</h2>
        <p>
          I am a passionate and results-driven software developer with a strong foundation in computer science and a keen interest in artificial intelligence and machine learning. My journey in tech has been fueled by a desire to solve complex problems and build innovative solutions that can make a tangible impact.
        </p>
        <p>
          Currently, I'm focused on expanding my expertise in full-stack development, cloud technologies (AWS), and deploying scalable AI models. I believe in continuous learning and am always exploring new tools and frameworks to enhance my skill set.
        </p>
        <p>
          This microsite serves as a small portfolio and a space to share my projects and thoughts. Feel free to explore my skills and the projects I've been working on.
        </p>
        {/* Placeholder for an image
        <div className={styles.profileImageContainer}>
          <img src="/path-to-your-image.jpg" alt="Yuri Oliveira" className={styles.profileImage} />
        </div>
        */}
      </section>

      {/* Integrate WaitlistForm here */}
      <section className={styles.waitlistSection}>
        <WaitlistForm />
      </section>

      <section className={styles.ctaSection}>
        <h2>Get in Touch or See More</h2>
        <p>
          I'm always open to discussing new projects, collaborations, or opportunities.
        </p>
        <div className={styles.ctaButtons}>
          <Link href="/projects" legacyBehavior>
            <a className="button">View My Projects</a>
          </Link>
          <Link href="/skills" legacyBehavior>
            <a className="button button-secondary">Explore My Skills</a>
          </Link>
          {/* Future CTA:
          <Link href="/contact" legacyBehavior>
            <a className="button">Contact Me</a>
          </Link>
          */}
        </div>
      </section>
    </div>
  );
}
