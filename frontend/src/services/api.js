/**
 * API service for communicating with the backend.
 */

const API_BASE_URL = '/api';

/**
 * Generate a natal chart based on birth information.
 * @param {Object} birthData - Birth information
 * @param {string} birthData.date - Birth date in YYYY-MM-DD format
 * @param {string} birthData.time - Birth time in HH:MM format
 * @param {string} birthData.country - Birth country
 * @param {string} birthData.city - Birth city
 * @returns {Promise<Object>} Natal chart data
 * @throws {Error} If the API request fails
 */
export async function generateChart(birthData) {
  const response = await fetch(`${API_BASE_URL}/chart`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(birthData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage =
      errorData.detail || `HTTP error! status: ${response.status}`;
    throw new Error(errorMessage);
  }

  return response.json();
}

/**
 * Check API health.
 * @returns {Promise<Object>} Health status
 * @throws {Error} If the API request fails
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}
