import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile"; 
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from "./component/ProtectedRoute";

// Wrapper components to avoid repeating AuthProvider + ProtectedRoute
const AppWrapper = (
  <AuthProvider>
    <App />
  </AuthProvider>
);

const LoginWrapper = (
  <AuthProvider>
    <Login />
  </AuthProvider>
);

const DashboardWrapper = (
  <AuthProvider>
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  </AuthProvider>
);

const ProfileWrapper = (
  <AuthProvider>
    <ProtectedRoute>
      <Profile />
    </ProtectedRoute>
  </AuthProvider>
);

// Define routes
const router = createBrowserRouter([
  { path: "/", element: AppWrapper },
  { path: "/login", element: LoginWrapper },
  { path: "/dashboard", element: DashboardWrapper },
  { path: "/profile", element: ProfileWrapper }, 
]);

// Render app
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
