import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'

export default function ProjectsList() {
  const [projects, setProjects] = useState([])

  useEffect(() => {
    api.get('/projects').then(res => setProjects(res.data)).catch(console.error)
  }, [])

  return (
    <div>
      <h3>Projetos</h3>
      <ul>
        {projects.map(p => (
          <li key={p.id}>
            <Link to={`/projects/${p.id}`}>{p.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
