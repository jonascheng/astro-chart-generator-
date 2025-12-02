import { useState } from 'react';
import NatalChart from '../components/NatalChart';
import './ChartPage.css';

export default function ChartPage() {
  const [formData, setFormData] = useState({
    date: '',
    time: '',
    country: '',
    city: '',
  });

  const [chartData, setChartData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  // Validate form fields
  const validateForm = () => {
    const errors = {};

    if (!formData.date) {
      errors.date = 'Birth date is required';
    } else {
      // Verify date is not in the future
      const selectedDate = new Date(formData.date);
      const today = new Date();
      if (selectedDate > today) {
        errors.date = 'Birth date cannot be in the future';
      }
      // Verify date is not before 1900
      if (selectedDate.getFullYear() < 1900) {
        errors.date = 'Birth date must be after 1900';
      }
    }

    if (!formData.time) {
      errors.time = 'Birth time is required';
    }

    if (!formData.country || formData.country.trim() === '') {
      errors.country = 'Country is required';
    }

    if (!formData.city || formData.city.trim() === '') {
      errors.city = 'City is required';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear validation error for this field when user starts typing
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validate form before submission
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Convert time from HH:MM to HH:MM:SS format for backend
      const dataToSend = {
        ...formData,
        time: formData.time ? `${formData.time}:00` : formData.time,
      };

      const response = await fetch('/api/chart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });

      if (!response.ok) {
        let errorMessage = 'An error occurred while generating your chart';
        try {
          const errorData = await response.json();
          // Handle both FastAPI validation errors and custom errors
          if (errorData.detail) {
            if (Array.isArray(errorData.detail)) {
              // Pydantic validation errors
              errorMessage = errorData.detail
                .map(
                  (err) =>
                    `${err.loc[err.loc.length - 1]}: ${err.msg}`
                )
                .join(', ');
            } else {
              // Custom error messages from endpoint
              errorMessage = errorData.detail;
            }
          }
        } catch {
          // Fallback if response is not JSON
          errorMessage = `HTTP error! Status: ${response.status}`;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setChartData(data);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching the chart');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chart-page-container">
      <div className="chart-page-header">
        <h1>Natal Chart Generator</h1>
        <p>Enter your birth information to generate your natal chart</p>
      </div>

      <div className="chart-page-content">
        <form onSubmit={handleSubmit} className="chart-form" noValidate>
          <div className="form-group">
            <label htmlFor="date">Birth Date *</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleInputChange}
              className={`form-input ${validationErrors.date ? 'form-input-error' : ''}`}
              aria-describedby={validationErrors.date ? 'date-error' : undefined}
            />
            {validationErrors.date && (
              <span className="validation-error" id="date-error">
                {validationErrors.date}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="time">Birth Time *</label>
            <input
              type="time"
              id="time"
              name="time"
              value={formData.time}
              onChange={handleInputChange}
              className={`form-input ${validationErrors.time ? 'form-input-error' : ''}`}
              aria-describedby={validationErrors.time ? 'time-error' : undefined}
            />
            {validationErrors.time && (
              <span className="validation-error" id="time-error">
                {validationErrors.time}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="country">Country *</label>
            <input
              type="text"
              id="country"
              name="country"
              value={formData.country}
              onChange={handleInputChange}
              placeholder="e.g., USA"
              className={`form-input ${validationErrors.country ? 'form-input-error' : ''}`}
              aria-describedby={validationErrors.country ? 'country-error' : undefined}
            />
            {validationErrors.country && (
              <span className="validation-error" id="country-error">
                {validationErrors.country}
              </span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="city">City *</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleInputChange}
              placeholder="e.g., New York"
              className={`form-input ${validationErrors.city ? 'form-input-error' : ''}`}
              aria-describedby={validationErrors.city ? 'city-error' : undefined}
            />
            {validationErrors.city && (
              <span className="validation-error" id="city-error">
                {validationErrors.city}
              </span>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="submit-button"
          >
            {isLoading ? 'Generating Chart...' : 'Generate Chart'}
          </button>
        </form>

        <div className="chart-results">
          {error && (
            <div className="error-message">
              <p>Error: {error}</p>
            </div>
          )}

          {chartData && (
            <>
              <NatalChart chartData={chartData} />
            </>
          )}

          {!chartData && !error && (
            <div className="empty-state">
              <p>Fill out the form and click "Generate Chart" to see your natal chart</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
