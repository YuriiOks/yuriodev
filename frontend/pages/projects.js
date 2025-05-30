import Head from 'next/head';
import styles from '../styles/Projects.module.css';
import Link from 'next/link';

// This is for setting the page title in _app.js
Projects.title = "Projects | Yuri Oliveira";

const projectData = [
  {
    title: "AI-Powered Content Summarizer",
    description: "A web application that uses Natural Language Processing to generate concise summaries of long texts or articles. Built with Python (FastAPI) for the backend and Next.js for the frontend.",
    tags: ["AI/ML", "NLP", "Python", "FastAPI", "Next.js", "Docker"],
    liveLink: "#", // Replace with actual link if available
    sourceLink: "#" // Replace with actual link if available
  },
  {
    title: "Interactive Data Visualization Dashboard",
    description: "A dashboard for visualizing complex datasets with interactive charts and filters. Developed using React, D3.js, and connected to a data API.",
    tags: ["Data Visualization", "React", "D3.js", "JavaScript", "API Integration"],
    liveLink: "#",
    sourceLink: "#"
  },
  {
    title: "Personal Portfolio & Blog Platform (This Site!)",
    description: "The very platform you are currently viewing! A full-stack application built with Next.js for the frontend, and planned integration with a headless CMS or custom backend for blog content and project management.",
    tags: ["Next.js", "React", "Node.js", "CI/CD", "Responsive Design"],
    liveLink: "/",
    sourceLink: "#" // Link to GitHub repo if public
  }
];

export default function Projects() {
  return (
    <div className={styles.container}>
      <Head>
        <meta name="description" content="Discover projects by Yuri Oliveira, showcasing skills in AI, web development, and more." />
      </Head>

      <header className={styles.header}>
        <h1>My Projects</h1>
        <p>A selection of projects I've worked on, demonstrating my skills and interests.</p>
      </header>

      <div className={styles.projectsGrid}>
        {projectData.map((project) => (
          <article key={project.title} className={`card ${styles.projectCard}`}> {/* Using global .card style */}
            <h3>{project.title}</h3>
            <p className={styles.projectDescription}>{project.description}</p>
            <div className={styles.projectTags}>
              {project.tags.map(tag => (
                <span key={tag} className={styles.tag}>{tag}</span>
              ))}
            </div>
            <div className={styles.projectLinks}>
              {project.liveLink && project.liveLink !== "#" && (
                <Link href={project.liveLink} legacyBehavior>
                  <a target="_blank" rel="noopener noreferrer" className="button">View Live</a>
                </Link>
              )}
              {project.sourceLink && project.sourceLink !== "#" && (
                <Link href={project.sourceLink} legacyBehavior>
                  <a target="_blank" rel="noopener noreferrer" className="button button-secondary">Source Code</a>
                </Link>
              )}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
