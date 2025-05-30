import Head from 'next/head';
import styles from '../styles/Blog.module.css'; // We'll create this CSS module

// This is for setting the page title in _app.js
Blog.title = "Blog | Yuri Oliveira";

export default function Blog() {
  return (
    <div className={styles.container}>
      <Head>
        <meta name="description" content="Blog and articles by Yuri Oliveira on software development, AI, and technology." />
      </Head>

      <header className={styles.header}>
        <h1>My Blog</h1>
        <p>Thoughts, tutorials, and insights on the world of technology.</p>
      </header>

      <section className={styles.content}>
        <h2>Coming Soon!</h2>
        <p>
          I'm currently working on curating content for this blog. Soon, you'll find articles about software development,
          AI/ML, best practices, tutorials, and my personal experiences in the tech industry.
        </p>
        <p>
          In the meantime, you can connect with me on other platforms or check out my projects.
        </p>
        {/*
          Placeholder for linking to an external blog if decided later:
          <div className={styles.externalBlogLink}>
            <p>You can also find my articles on Medium:</p>
            <a href="https://medium.com/@yourusername" target="_blank" rel="noopener noreferrer" className="button">
              Visit My Medium Profile
            </a>
          </div>
        */}
      </section>
    </div>
  );
}
