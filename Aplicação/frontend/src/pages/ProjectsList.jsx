import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useProjects } from '../api/projects'

export default function ProjectsList() {
  const { projects, loading, error, fetchProjects } = useProjects()

  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  if (loading) {
    return (
      <div>
        <h3>Projetos</h3>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800">Erro ao carregar projetos: {error}</p>
        <button 
          onClick={() => fetchProjects()}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Tentar novamente
        </button>
      </div>
    )
  }

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
