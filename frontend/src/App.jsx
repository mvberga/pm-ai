import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import ProjectsList from './pages/ProjectsList'
import ProjectDetail from './pages/ProjectDetail'
import { PortfolioOverview } from './components/dashboard/PortfolioOverview'

export default function App() {
  return (
    <div style={{padding: 16, fontFamily: 'system-ui, Arial'}}>
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <h2>PM AI MVP</h2>
        <nav style={{display: 'flex', gap: 12}}>
          <Link to="/">Dashboard</Link>
          <Link to="/projects">Projetos</Link>
        </nav>
      </header>
      <main style={{marginTop: 16}}>
        <Routes>
          <Route path="/" element={<PortfolioOverview />} />
          <Route path="/projects" element={<ProjectsList />} />
          <Route path="/projects/:id" element={<ProjectDetail />} />
        </Routes>
      </main>
    </div>
  )
}
