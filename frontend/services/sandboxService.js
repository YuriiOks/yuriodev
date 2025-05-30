// Get the API base URL from environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

/**
 * Executes Python code on the backend.
 * @param {string} code - The Python code to execute.
 * @returns {Promise<Object>} A promise that resolves to an object containing output, error, execution_time, etc.
 * @throws {Error} If the network response is not ok or if the request fails.
 */
export const executeCode = async (code) => {
  if (typeof code !== 'string') {
    throw new Error("Code must be a string.");
  }

  const response = await fetch(`${API_BASE_URL}/sandbox/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Cookies (including JWT for authentication) will be sent automatically by the browser
      // if the request is to the same origin or CORS is configured for credentials.
    },
    body: JSON.stringify({ code: code, language: "python" }), // language field is for future use
  });

  if (!response.ok) {
    let errorDetail = "Failed to execute code.";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {
      // Ignore if response is not JSON
    }
    console.error("Error executing code:", response.status, errorDetail);
    // Throw an error that can be caught by the calling component
    const err = new Error(errorDetail);
    err.status = response.status; // Attach status code to error object
    throw err;
  }

  return response.json(); // Returns { output, error, execution_time, success, exit_code }
};
