import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/client'
import Checklist from '../components/Checklist'
import ActionItems from '../components/ActionItems'

export default function ProjectDetail() {
  const { id } = useParams()
  const [project, setProject] = useState(null)
  const [tab, setTab] = useState('checklist')

  useEffect(() => {
    api.get(`/projects/${id}`).then(res => setProject(res.data)).catch(console.error)
  }, [id])

  if (!project) return <div>Carregando...</div>

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
