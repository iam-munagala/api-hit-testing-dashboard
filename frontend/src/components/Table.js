import React, { useState } from 'react';
import ReactPaginate from 'react-paginate';

const Table = ({ data }) => {
  const [filter, setFilter] = useState('');
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(0);
  const [timestampFilter, setTimestampFilter] = useState('');
  const [userAgentFilter, setUserAgentFilter] = useState('');

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
    setCurrentPage(0); // Reset to first page when filter changes
  };

  const handleItemsPerPageChange = (event) => {
    setItemsPerPage(parseInt(event.target.value));
    setCurrentPage(0); // Reset to first page when items per page changes
  };

  const handlePageChange = (event) => {
    setCurrentPage(event.selected);
  };

  const filteredData = data.filter(item =>
    (!filter || item.request_type === filter) &&
    (!timestampFilter || item.timestamp.toLowerCase().includes(timestampFilter.toLowerCase())) &&
    (!userAgentFilter || item.user_agent.toLowerCase().includes(userAgentFilter.toLowerCase()))
  );

  const pageCount = Math.ceil(filteredData.length / itemsPerPage);
  const displayedData = filteredData.slice(currentPage * itemsPerPage, (currentPage + 1) * itemsPerPage);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between mb-4">
        <div>
          <label className="mr-2 font-bold">Filter by Request Type:</label>
          <select value={filter} onChange={handleFilterChange} className="border rounded p-1">
            <option value="">All</option>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
          </select>
        </div>
        <div>
          <label className="mr-2 font-bold">Items per Page:</label>
          <select value={itemsPerPage} onChange={handleItemsPerPageChange} className="border rounded p-1">
            <option value={10}>10</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </div>
      </div>
      <div className="flex justify-between mb-4">
        <div>
          <label className="mr-2 font-bold">Filter by Timestamp:</label>
          <input
            type="text"
            value={timestampFilter}
            onChange={(e) => setTimestampFilter(e.target.value)}
            className="border rounded p-1"
            placeholder="Filter by Timestamp"
          />
        </div>
        <div>
          <label className="mr-2 font-bold">Filter by User Agent:</label>
          <input
            type="text"
            value={userAgentFilter}
            onChange={(e) => setUserAgentFilter(e.target.value)}
            className="border rounded p-1"
            placeholder="Filter by User Agent"
          />
        </div>
      </div>
      <table className="min-w-full bg-white border">
        <thead className="bg-gray-200">
          <tr>
            <th className="py-2 px-4 border-b-2 border-gray-300 font-semibold">ID</th>
            <th className="py-2 px-4 border-b-2 border-gray-300 font-semibold">Request Type</th>
            <th className="py-2 px-4 border-b-2 border-gray-300 font-semibold">Endpoint</th>
            <th className="py-2 px-4 border-b-2 border-gray-300 font-semibold">User Agent</th>
            <th className="py-2 px-4 border-b-2 border-gray-300 font-semibold">Request Body</th>
            <th className="py-2 px-4 border-b-2 border-gray-300 font-semibold">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {displayedData.map(item => (
            <tr key={item.id} className="even:bg-gray-100">
              <td className="py-2 px-4 border-b border-gray-200">{item.id}</td>
              <td className="py-2 px-4 border-b border-gray-200">{item.request_type}</td>
              <td className="py-2 px-4 border-b border-gray-200">{item.endpoint}</td>
              <td className="py-2 px-4 border-b border-gray-200">{item.user_agent}</td>
              <td className="py-2 px-4 border-b border-gray-200">{item.request_body}</td>
              <td className="py-2 px-4 border-b border-gray-200">{item.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4">
        <ReactPaginate
          pageCount={pageCount}
          pageRangeDisplayed={3}
          marginPagesDisplayed={2}
          onPageChange={handlePageChange}
          containerClassName="flex justify-center space-x-2"
          pageClassName="border rounded p-2"
          activeClassName="bg-blue-500 text-white"
          previousLabel="< Previous"
          nextLabel="Next >"
          previousClassName="border rounded p-2"
          nextClassName="border rounded p-2"
          disabledClassName="opacity-50"
        />
      </div>
    </div>
  );
};

export default Table;
