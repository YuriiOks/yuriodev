import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Head from 'next/head';
import { getCourses } from '../../services/courseService'; // Adjust path as needed
import styles from '../../styles/CourseCatalog.module.css'; // CSS module for this page
// Ensure Layout is used via _app.js, or import it here if not.

// Set page title for Layout component
CourseCatalogPage.title = "Courses | YuriODev Platform";

export default function CourseCatalogPage() {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCourses() {
      setIsLoading(true);
      try {
        const data = await getCourses(0, 20, true); // Fetch up to 20 published courses
        setCourses(data);
      } catch (err) {
        setError(err.message || "Failed to load courses.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadCourses();
  }, []);

  if (isLoading) {
    return <div className={styles.loadingState}>Loading courses...</div>;
  }

  if (error) {
    return <div className={styles.errorState}>Error: {error}</div>;
  }

  if (courses.length === 0) {
    return <div className={styles.emptyState}>No courses available at the moment. Please check back later!</div>;
  }

  return (
    <div className={styles.catalogContainer}>
      <Head>
        <title>{CourseCatalogPage.title}</title>
        <meta name="description" content="Explore software development courses on the YuriODev Platform." />
      </Head>

      <header className={styles.catalogHeader}>
        <h1>Course Catalog</h1>
        <p>Discover our range of courses designed to boost your software development skills.</p>
      </header>

      <div className={styles.courseGrid}>
        {courses.map((course) => (
          <div key={course.id} className={`card ${styles.courseCard}`}> {/* Using global .card and local styles */}
            {course.image_url && (
              <div className={styles.courseImageContainer}>
                <img src={course.image_url} alt={course.title} className={styles.courseImage} />
              </div>
            )}
            <div className={styles.courseContent}>
              <h3>{course.title}</h3>
              <p className={styles.courseDescription}>{course.description || 'No description available.'}</p>
              <Link href={`/courses/${course.slug}`} legacyBehavior>
                <a className={`button ${styles.detailsButton}`}>View Details</a>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
