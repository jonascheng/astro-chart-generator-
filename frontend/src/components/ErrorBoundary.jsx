import { Component } from 'react';
import PropTypes from 'prop-types';
import './ErrorBoundary.css';

/**
 * Error boundary component to catch unexpected errors in child components
 * and display a user-friendly error message with recovery options.
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary-container">
          <div className="error-boundary-content">
            <h2>Something went wrong</h2>
            <p>An unexpected error occurred. Please try again.</p>
            <details className="error-details">
              <summary>Error details</summary>
              <pre>{this.state.error?.toString()}</pre>
            </details>
            <button onClick={this.handleReset} className="error-boundary-button">
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
};

export default ErrorBoundary;
