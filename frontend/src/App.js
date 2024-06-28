import React from 'react';
import Dashboard from './components/Dashboard';
import './index.css'; // Ensure you have Tailwind CSS imported here

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">API Hit Tracking Dashboard</h1>
        <Dashboard />
      </div>
    </div>
  );
};

export default App;
