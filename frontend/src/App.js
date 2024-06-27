import React from 'react';
import Dashboard from './components/Dashboard';
import ErrorBoundary from './utils/ErrorBoundary';

function App() {
  return (
    <div className="container mx-auto p-4">
      <ErrorBoundary>
        <Dashboard />
      </ErrorBoundary>
    </div>
  );
}

export default App;
