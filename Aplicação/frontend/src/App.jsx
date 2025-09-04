import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import ProjectsList from './pages/ProjectsList'
import ProjectDetail from './pages/ProjectDetail'
import ProjectsStatusPage from './pages/ProjectsStatusPage'
import { PortfolioOverview } from './components/dashboard/PortfolioOverview'
import { DarkModeToggle } from './components/DarkModeToggle'

export default function App() {
  return (
    <div className="min-h-screen bg-secondary-50 dark:bg-secondary-900 transition-colors duration-200">
      <header className="bg-white dark:bg-secondary-800 shadow-sm border-b border-secondary-200 dark:border-secondary-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gradient">PM AI MVP</h1>
            </div>
            <div className="flex items-center space-x-4">
              <nav className="flex space-x-8">
                <Link 
                  to="/" 
                  className="text-secondary-600 dark:text-secondary-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors duration-200"
                >
                  Dashboard
                </Link>
                <Link 
                  to="/projects" 
                  className="text-secondary-600 dark:text-secondary-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors duration-200"
                >
                  Projetos
                </Link>
                <Link 
                  to="/projects/status" 
                  className="text-secondary-600 dark:text-secondary-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors duration-200"
                >
                  Status
                </Link>
              </nav>
              <DarkModeToggle />
            </div>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<PortfolioOverview />} />
          <Route path="/projects" element={<ProjectsList />} />
          <Route path="/projects/:id" element={<ProjectDetail />} />
          <Route path="/projects/status" element={<ProjectsStatusPage />} />
        </Routes>
      </main>
    </div>
  )
}
