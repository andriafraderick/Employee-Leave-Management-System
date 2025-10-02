import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

function App() {
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to login page immediately when component mounts
    navigate('/login');
  }, [navigate]);

  return null; 
}

export default App;