import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';
import PieChart from './PieChart';
import BarChart from './BarChart';
import Table from './Table';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiService.get('/api/hits/stats')
      .then(response => setData(response.data))
      .catch(error => setError(error));
  }, []);

  if (error) return <div className="text-red-500">Error fetching stats: {error.message}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="space-y-4 p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="h-64 md:h-auto">
          <BarChart data={data.barChartData} />
        </div>
        <div className="h-64 md:h-auto">
          <PieChart data={data.pieChartData} />
        </div>
      </div>
      <div className="mt-4">
        <Table data={data.tableData} />
      </div>
    </div>
  );
};

export default Dashboard;
