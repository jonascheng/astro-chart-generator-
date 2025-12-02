import ChartPage from './pages/ChartPage';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css';

function App() {
  return (
    <ErrorBoundary>
      <ChartPage />
    </ErrorBoundary>
  );
}

export default App;