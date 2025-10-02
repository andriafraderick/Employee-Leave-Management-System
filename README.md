# Employee Leave Management System

A full-stack web application for managing employee leave requests, approvals, and tracking built with FastAPI backend and React Vite frontend.

## 📋 Overview

This system automates the process of managing employee leave requests, approvals, and tracking, improving transparency and reducing manual overhead in organizations. It provides a centralized platform for employees to manage their leave applications and for administrators to track leave balances.

## 🚀 Features

### Core Functionality
- **User Authentication** - JWT-based secure login system
- **Leave Management** - Apply, track, and manage leave requests
- **Leave Type Categorization** - Casual, sick, emergency leaves
- **Real-time Dashboard** - View leave summaries and balances
- **Pagination** - Efficient data handling for large datasets
- **Search & Filter** - Find employees by ID, name, month, and year

### User Features
- Employee profile management
- Leave application submission
- Leave history tracking
- Real-time leave balance updates
- Monthly leave summaries

## 🛠 Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Python ORM for database interactions
- **Pydantic** - Data validation and settings management
- **JWT** - JSON Web Tokens for authentication
- **Python 3.8+** - Programming language

### Frontend
- **React** - JavaScript library for UI
- **Vite** - Fast build tool and development server
- **Material UI (MUI)** - React component library
- **Axios** - HTTP client for API calls
- **React Router** - Navigation and routing

### Development Tools
- **Postman** - API testing
- **Navicat** - Database management

## 📁 System Architecture
Client (React Vite) ↔ REST API (FastAPI) ↔ Database (PostgreSQL)

### Data Flow
1. User interacts with React frontend
2. Frontend makes API calls to FastAPI backend using Axios
3. Backend processes requests with JWT authentication
4. SQLAlchemy ORM interacts with PostgreSQL database
5. Response sent back to frontend for UI updates

## 🗃 Database Schema

The system uses PostgreSQL with the following main tables:

### Core Tables
- **users** - Employee information (name, email, designation, role, manager)
- **leave_applications** - Leave requests with status, duration, and reasons
- **leave_types** - Categories of leaves (casual, sick, emergency)
- **leave_details** - Employee entitlements per leave type
- **remaining_leaves** - Total and remaining leaves per employee per year
- **profiles** - Extended employee profile information

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL
- Git
API Endpoints
Authentication
POST /token - User login and JWT token generation

Leave Management
GET /combined/all_leave_details - Get comprehensive leave data

POST /leave-applications - Submit new leave application

GET /leave-applications - Get leave applications with filters

User Management
GET /users - Get user information

GET /profiles - Get employee profiles

🎯 Usage
Employee Login
Access the application through the browser

Login with employee credentials

View dashboard with leave summary

Apply for leave using the application form

Track application status and leave balances

Features Demonstrated
Dashboard: Monthly leave summaries with pagination

Search: Filter employees by ID or name

Tooltips: Detailed leave breakdowns on hover

Pagination: Navigate through large datasets efficiently

🎓 Learning Outcomes
This project demonstrates practical experience in:

FastAPI - Modular project structure with routers, models, and schemas

JWT Authentication - Secure token-based authentication system

React Development - Component-based UI with state management

Database Design - Complex SQLAlchemy queries and table relationships

API Integration - Axios for frontend-backend communication

UI/UX - Material UI for responsive and clean interfaces

Pagination - Backend limit/offset with frontend pagination components

🔮 Future Enhancements
Admin dashboard with advanced analytics

Role-based access control (RBAC)

Automated email notifications

Leave approval workflows

Advanced reporting and analytics

Mobile application

Integration with calendar systems

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

