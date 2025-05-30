// Get the API base URL from environment variables, with a fallback for local development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

/**
 * Fetches a list of courses from the backend.
 * @param {number} skip - Number of courses to skip (for pagination).
 * @param {number} limit - Maximum number of courses to return.
 * @param {boolean} published_only - Whether to fetch only published courses.
 * @returns {Promise<Array>} A promise that resolves to an array of courses.
 * @throws {Error} If the network response is not ok.
 */
export const getCourses = async (skip = 0, limit = 10, published_only = true) => {
  const queryParams = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
    published_only: published_only.toString(),
  });

  const response = await fetch(`${API_BASE_URL}/courses?${queryParams}`);

  if (!response.ok) {
    // Log the error or handle it more gracefully
    const errorData = await response.json().catch(() => ({ detail: "Failed to fetch courses and error response is not JSON" }));
    console.error("Error fetching courses:", response.status, errorData);
    // throw new Error(errorData.detail || `Failed to fetch courses. Status: ${response.status}`);
    return []; // Return empty array on error for getStaticPaths
  }
  return response.json();
};

/**
 * Fetches a single lesson by its ID from the backend.
 * @param {string|number} lessonId - The ID of the lesson to fetch.
 * @returns {Promise<Object>} A promise that resolves to the lesson object.
 * @throws {Error} If the network response is not ok.
 */
export const getLessonById = async (lessonId) => {
  if (!lessonId) {
    throw new Error("Lesson ID is required to fetch a lesson.");
  }
  const response = await fetch(`${API_BASE_URL}/lessons/${lessonId}`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: `Failed to fetch lesson '${lessonId}' and error response is not JSON` }));
    console.error(`Error fetching lesson '${lessonId}':`, response.status, errorData);
    if (response.status === 404) {
        throw new Error(errorData.detail || `Lesson with ID '${lessonId}' not found.`);
    }
    throw new Error(errorData.detail || `Failed to fetch lesson '${lessonId}'. Status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetches a single course by its slug from the backend.
 * @param {string} slug - The slug of the course to fetch.
 * @returns {Promise<Object>} A promise that resolves to the course object.
 * @throws {Error} If the network response is not ok (e.g., 404 Not Found).
 */
export const getCourseBySlug = async (slug) => {
  if (!slug) {
    throw new Error("Slug is required to fetch a course.");
  }
  const response = await fetch(`${API_BASE_URL}/courses/${slug}`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: `Failed to fetch course '${slug}' and error response is not JSON` }));
    console.error(`Error fetching course '${slug}':`, response.status, errorData);
    // if (response.status === 404) {
    //     throw new Error(errorData.detail || `Course with slug '${slug}' not found.`);
    // }
    // throw new Error(errorData.detail || `Failed to fetch course '${slug}'. Status: ${response.status}`);
    return null; // Return null on error for getStaticProps
  }
  return response.json();
};
