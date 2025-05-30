import React from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { getCourseBySlug, getCourses } from '../../services/courseService'; // Adjust path as needed
import styles from '../../styles/CourseDetail.module.css'; // Create this CSS module

// This sets the page title in the Layout component via _app.js
// We'll set it dynamically in the component based on course data.

// This function is needed by Next.js for dynamic pages that use `getStaticProps`
// It tells Next.js which paths should be pre-rendered at build time.
export async function getStaticPaths() {
  // Fetch a list of all course slugs to pre-render those pages
  // In a real app, you might only pre-render popular courses or a subset.
  // For now, fetch all published courses.
  // try {
  //   const courses = await getCourses(0, 100, true); // Fetch up to 100 published courses for paths
  //   const paths = courses.map((course) => ({
  //     params: { slug: course.slug },
  //   }));
  //   return { paths, fallback: 'blocking' }; // 'blocking' means SSR for non-pre-rendered paths
  // } catch (error) {
  //   console.error("Error fetching paths for courses:", error);
  //   return { paths: [], fallback: 'blocking' }; // Fallback to SSR on error
  // }
  // To ensure build completes without backend, always return empty paths and use fallback.
  return { paths: [], fallback: 'blocking' };
}

// This function fetches data for a specific course page at build time or request time (SSR/ISR)
export async function getStaticProps({ params }) {
  // try {
  const course = await getCourseBySlug(params.slug);
  if (!course) { // courseService now returns null on error/not found
    return { notFound: true }; // Returns a 404 page if course not found
  }
  return {
    props: { course },
    revalidate: 60 * 10 // Revalidate every 10 minutes (Incremental Static Regeneration)
  };
  // } catch (error) { // Error should be handled by courseService returning null
  //   console.error(`Error fetching course ${params.slug}:`, error);
  //   return { notFound: true };
  // }
}


export default function CourseDetailPage({ course }) {
  const router = useRouter();

  // If fallback is true and the page is not yet generated
  if (router.isFallback) {
    return <div className={styles.loadingState}>Loading course...</div>;
  }

  // This case should be handled by getStaticProps returning notFound: true
  if (!course) {
    return <div className={styles.errorState}>Course not found.</div>;
  }

  // Set dynamic page title (can be done in Head component too)
  // If Layout takes title from Component.title, this needs to be set differently for dynamic pages.
  // For now, using Head directly is simpler for dynamic titles.

  return (
    <div className={styles.detailContainer}>
      <Head>
        <title>{course.title} | YuriODev Platform</title>
        <meta name="description" content={course.description || `Details for the course: ${course.title}`} />
      </Head>

      <article className={styles.courseArticle}>
        <header className={styles.courseHeader}>
          <h1>{course.title}</h1>
          {course.image_url && (
            <img src={course.image_url} alt={course.title} className={styles.courseImage} />
          )}
          <p className={styles.courseDescription}>{course.description}</p>
          {/* Add other metadata like instructor, duration, last updated etc. if available */}
        </header>

        <section className={styles.modulesSection}>
          <h2>Modules</h2>
          {course.modules && course.modules.length > 0 ? (
            <ul className={styles.moduleList}>
              {course.modules.map((module) => (
                <li key={module.id} className={styles.moduleItem}>
                  <h3>{module.title}</h3>
                  {module.description && <p className={styles.moduleDescription}>{module.description}</p>}
                  {module.lessons && module.lessons.length > 0 ? (
                    <ul className={styles.lessonList}>
                      {module.lessons.map((lesson) => (
                        <li key={lesson.id} className={styles.lessonItem}>
                          <Link href={`/courses/${course.slug}/lessons/${lesson.id}`} legacyBehavior>
                            <a className={styles.lessonLink}>
                              {lesson.order + 1}. {lesson.title}
                              <span className={styles.lessonType}>({lesson.content_type})</span>
                            </a>
                          </Link>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className={styles.noLessons}>No lessons in this module yet.</p>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p>No modules available for this course yet.</p>
          )}
        </section>
      </article>

      <div className={styles.backLinkContainer}>
        <Link href="/courses" legacyBehavior>
          <a className="button button-secondary">&larr; Back to Course Catalog</a>
        </Link>
      </div>
    </div>
  );
}
