import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import NatalChart from '../components/NatalChart';
import PositionsTable from '../components/PositionsTable';
import './ChartPage.css';

export default function ChartPage() {
  const { t } = useTranslation();
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
      errors.date = t('error_missing_field');
    } else {
      // Verify date is not in the future
      const selectedDate = new Date(formData.date);
      const today = new Date();
      if (selectedDate > today) {
        errors.date = t('error_invalid_date');
      }
      // Verify date is not before 1900
      if (selectedDate.getFullYear() < 1900) {
        errors.date = t('error_invalid_date');
      }
    }

    if (!formData.time) {
      errors.time = t('error_missing_field');
    }

    if (!formData.country || formData.country.trim() === '') {
      errors.country = t('error_missing_field');
    }

    if (!formData.city || formData.city.trim() === '') {
      errors.city = t('error_missing_field');
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

  const handleRetry = () => {
    setError(null);
    setChartData(null);
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
        let errorMessage = t('error_api_failed');
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
      setError(err.message || t('error_api_failed'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chart-page-container">
      <div className="chart-page-header">
        <h1>{t('app_title')}</h1>
        <p>{t('form_description')}</p>
      </div>

      <div className="chart-page-content">
        <form onSubmit={handleSubmit} className="chart-form" noValidate>
          <div className="form-group">
            <label htmlFor="date">{t('label_birth_date')} *</label>
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
            <label htmlFor="time">{t('label_birth_time')} *</label>
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
            <label htmlFor="country">{t('label_birth_location')} *</label>
            <input
              type="text"
              id="country"
              name="country"
              value={formData.country}
              onChange={handleInputChange}
              placeholder={t('placeholder_birth_location')}
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
            <label htmlFor="city">{t('label_birth_location')} *</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleInputChange}
              placeholder={t('placeholder_birth_location')}
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
            {isLoading ? t('loading') : t('button_generate_chart')}
          </button>
        </form>

        <div className="chart-results">
          {error && (
            <div className="error-container">
              <div className="error-message">
                <h3>{t('error_api_failed')}</h3>
                <p>{error}</p>
                <button onClick={handleRetry} className="retry-button">
                  {t('retry')}
                </button>
              </div>
            </div>
          )}

          {chartData && (
            <>
              <div className="chart-actions">
                <button
                  type="button"
                  className="print-button"
                  onClick={() => window.print()}
                  aria-label={t('button_print_chart')}
                >
                  {t('button_print_chart')}
                </button>
              </div>
              <NatalChart chartData={chartData} />
              <PositionsTable planets={chartData.planets} points={chartData.points} />
            </>
          )}

          {!chartData && !error && (
            <div className="empty-state">
              <p>{t('form_description')}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
