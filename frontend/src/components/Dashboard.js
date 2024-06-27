import React, { useState, useEffect } from 'react';
import axios from '../services/apiService';
import PieChart from './PieChart';
import BarChart from './BarChart';
import Table from './Table';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/hits/stats')
      .then(response => setData(response.data))
      .catch(error => setError(error));
  }, []);

  if (error) return <div className="text-red-500">Error fetching stats: {error.message}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="space-y-4">
      <PieChart data={data.pieChartData} />
      <BarChart data={data.barChartData} />
      <Table data={data.tableData} />
    </div>
  );
};

export default Dashboard;
