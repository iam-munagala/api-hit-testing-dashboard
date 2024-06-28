import axios from 'axios';

const apiService = axios.create({
  baseURL: 'http://localhost:5000', // Adjust the baseURL as per your backend configuration
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiService;
