import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router'; // Not strictly needed if not using router instance directly
import { getLessonById } from '../../../../services/courseService'; // Corrected path
import LessonContent from '../../../../components/LessonContent'; // Corrected path
import styles from '../../../../styles/LessonDetailPage.module.css'; // Corrected path

// This function runs on the server side for every request
export async function getServerSideProps(context) {
  const { lessonId, slug: courseSlug } = context.params; // Get lessonId and courseSlug from URL params
  let lesson = null;
  let error = null;

  try {
    lesson = await getLessonById(lessonId);
  } catch (err) {
    console.error(`Error fetching lesson ${lessonId}:`, err);
    error = err.message || "Failed to load lesson.";
    if (err.message.includes("not found")) { // Basic check for 404 type error from service
        return { notFound: true }; // This will render the 404 page
    }
  }

  // If lesson is null and no specific error led to notFound, it might be a server error
  // or the service returned null without throwing a specific "not found" error.
  if (!lesson && !error) {
      // This ensures that if getLessonById returns null without throwing an error
      // that should be a 404, we still render a 404.
      return { notFound: true };
  }

  return {
    props: {
      lesson, // This will be null if an error occurred that wasn't a 404
      courseSlug, // Pass courseSlug to allow "back to course" navigation
      error, // Pass error message to the page
    },
  };
}

export default function LessonDetailPage({ lesson, courseSlug, error }) {
  // const router = useRouter(); // For fallback: true on getStaticProps, or other router uses

  if (error && !lesson) { // If there was an error and no lesson data
    return <div className={styles.errorState}>Error: {error}</div>;
  }

  // This case should ideally be handled by getServerSideProps returning notFound: true
  // or by the error check above.
  if (!lesson) {
    return <div className={styles.errorState}>Lesson data is not available.</div>;
  }

  return (
    <div className={styles.pageContainer}>
      <Head>
        <title>{lesson.title} | YuriODev Platform</title>
        {/* Add more meta tags as needed */}
      </Head>

      <nav className={styles.breadcrumbNav}>
        <Link href="/courses" legacyBehavior><a>Courses</a></Link>
        <span>&gt;</span>
        <Link href={`/courses/${courseSlug}`} legacyBehavior><a>{courseSlug}</a></Link>
        {/* Ideally, fetch course title for breadcrumb, but slug is okay for now */}
        <span>&gt;</span>
        <span>{lesson.title}</span>
      </nav>

      <main className={styles.lessonMainContent}>
        <h1 className={styles.lessonTitle}>{lesson.title}</h1>
        <LessonContent lesson={lesson} />
      </main>

      <nav className={styles.lessonNavigation}>
        {/* Placeholder for Previous/Next lesson links - requires more complex logic */}
        {/* <Link href="#" legacyBehavior><a className="button button-secondary">Previous Lesson</a></Link> */}
        <Link href={`/courses/${courseSlug}`} legacyBehavior>
          <a className={`button ${styles.backButton}`}>Back to Course Outline</a>
        </Link>
        {/* <Link href="#" legacyBehavior><a className="button button-secondary">Next Lesson</a></Link> */}
      </nav>
    </div>
  );
}
