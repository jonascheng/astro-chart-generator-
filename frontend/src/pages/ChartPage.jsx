import { useState } from 'react';
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/chart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
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
        <form onSubmit={handleSubmit} className="chart-form">
          <div className="form-group">
            <label htmlFor="date">Birth Date</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleInputChange}
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="time">Birth Time</label>
            <input
              type="time"
              id="time"
              name="time"
              value={formData.time}
              onChange={handleInputChange}
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="country">Country</label>
            <input
              type="text"
              id="country"
              name="country"
              value={formData.country}
              onChange={handleInputChange}
              placeholder="e.g., USA"
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="city">City</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleInputChange}
              placeholder="e.g., New York"
              required
              className="form-input"
            />
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
            <div className="chart-data">
              <h2>Chart Data</h2>
              <pre>{JSON.stringify(chartData, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
