import Head from 'next/head';
import styles from '../styles/Skills.module.css';

// This is for setting the page title in _app.js
Skills.title = "Skills | Yuri Oliveira";

const skillsData = [
  {
    category: "Programming Languages",
    items: ["Python", "JavaScript (ES6+)", "TypeScript", "SQL", "Java (Basic)", "C# (Basic)"]
  },
  {
    category: "AI & Machine Learning",
    items: ["Scikit-learn", "Pandas", "NumPy", "TensorFlow (Keras)", "Natural Language Processing (NLTK, spaCy)", "Data Visualization (Matplotlib, Seaborn)"]
  },
  {
    category: "Web Development - Backend",
    items: ["FastAPI", "Node.js", "Express.js", "RESTful APIs", "GraphQL (Basic)", "Django (Basic)"]
  },
  {
    category: "Web Development - Frontend",
    items: ["Next.js", "React", "HTML5", "CSS3", "Sass/SCSS", "Tailwind CSS (Familiar)", "Material-UI"]
  },
  {
    category: "Databases",
    items: ["PostgreSQL", "MongoDB", "MySQL", "SQLite", "Redis"]
  },
  {
    category: "DevOps & Cloud",
    items: ["Docker", "Kubernetes (Basic)", "AWS (EC2, S3, RDS, Lambda)", "Git & GitHub", "CI/CD (GitHub Actions)", "Linux/Unix"]
  },
  {
    category: "Tools & Methodologies",
    items: ["Agile/Scrum", "Jira", "VS Code", "Postman", "Unit Testing (Pytest, Jest)"]
  }
];

export default function Skills() {
  return (
    <div className={styles.container}>
      <Head>
        <meta name="description" content="Explore Yuri Oliveira's technical skills in AI/ML, web development, DevOps, and more." />
      </Head>

      <header className={styles.header}>
        <h1>My Technical Skills</h1>
        <p>A snapshot of the technologies and tools I work with.</p>
      </header>

      <div className={styles.skillsGrid}>
        {skillsData.map((skillCategory) => (
          <section key={skillCategory.category} className={`card ${styles.skillCategory}`}> {/* Using global .card style */}
            <h3>{skillCategory.category}</h3>
            <ul className={styles.skillList}>
              {skillCategory.items.map((skill) => (
                <li key={skill} className={styles.skillItem}>{skill}</li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
