import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { projectsApi } from '../api/projects'
import Checklist from '../components/Checklist'
import ActionItems from '../components/ActionItems'

export default function ProjectDetail() {
  const { id } = useParams()
  const [project, setProject] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [tab, setTab] = useState('checklist')

  useEffect(() => {
    const fetchProject = async () => {
      try {
        setLoading(true)
        setError(null)
        const projectData = await projectsApi.getById(Number(id))
        setProject(projectData)
      } catch (err) {
        setError(err.message || 'Erro ao carregar projeto')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      fetchProject()
    }
  }, [id])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800">Erro ao carregar projeto: {error}</p>
        <button 
          onClick={async () => {
            try {
              setLoading(true)
              setError(null)
              const projectData = await projectsApi.getById(Number(id))
              setProject(projectData)
            } catch (err) {
              setError(err.message || 'Erro ao carregar projeto')
            } finally {
              setLoading(false)
            }
          }}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Tentar novamente
        </button>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
        <p className="text-yellow-800">Projeto não encontrado.</p>
      </div>
    )
  }

  return (
    <div>
      <h3>{project.name}</h3>
      <p style={{opacity: 0.8}}>{project.description}</p>

      <div style={{display: 'flex', gap: 8, margin: '12px 0'}}>
        <button onClick={() => setTab('checklist')}>Checklist</button>
        <button onClick={() => setTab('actions')}>Central de Ações</button>
      </div>

      {tab === 'checklist' ? (
        <Checklist projectId={id} />
      ) : (
        <ActionItems projectId={id} />
      )}
    </div>
  )
}
