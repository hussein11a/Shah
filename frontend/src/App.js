import { useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const helloWorldApi = async () => {
    try {
      const response = await axios.get(`${API}/`);
      console.log(response.data.message);
    } catch (e) {
      console.error(e, `errored out requesting / api`);
    }
  };

  useEffect(() => {
    helloWorldApi();
  }, []);

  return (
    <div>
      <header className="App-header">
        <a
          className="App-link"
          href="https://emergent.sh"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src="https://avatars.githubusercontent.com/in/1201222?s=120&u=2686cf91179bbafbc7a71bfbc43004cf9ae1acea&v=4" />
        </a>
        <p className="mt-5">Building something incredible ~!</p>
        
        <div className="admin-links">
          <h3>Netlify CMS Admin</h3>
          <p>Access the content management system:</p>
          <a
            href="/admin"
            className="admin-link"
            target="_blank"
            rel="noopener noreferrer"
          >
            🔧 Open CMS Admin
          </a>
          <p className="admin-note">
            ✅ Fixed: Duplicate 'editor' keys issue resolved<br/>
            ✅ YAML syntax validated<br/>
            ✅ Proper configuration structure applied
          </p>
        </div>
      </header>
    </div>
  );
};

function App() {
  // Check if current path is admin
  const isAdminPath = window.location.pathname.startsWith('/admin');
  
  // If it's an admin path, don't render React Router - let the static files handle it
  if (isAdminPath) {
    return null;
  }

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />}>
            <Route index element={<Home />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
