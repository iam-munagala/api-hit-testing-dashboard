import React from 'react';

const Table = ({ data }) => {
  return (
    <table className="min-w-full bg-white border">
      <thead>
        <tr>
          {Object.keys(data[0]).map((key) => (
            <th key={key} className="py-2 px-4 border">{key}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {Object.values(row).map((value, i) => (
              <td key={i} className="py-2 px-4 border">{value}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Table;
