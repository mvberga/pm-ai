import React, { useEffect, useState } from 'react'
import api from '../api/client'

export default function ActionItems({ projectId }) {
  const [items, setItems] = useState([])
  const [filterType, setFilterType] = useState('')

  const fetchItems = () => {
    const q = filterType ? `?type=${encodeURIComponent(filterType)}` : ''
    api
      .get(`/projects/${projectId}/action-items${q}`)
      .then(res => setItems(res.data))
      .catch(err => {
        console.error(err)
      })
  }

  useEffect(() => {
    let cancelled = false
    const q = filterType ? `?type=${encodeURIComponent(filterType)}` : ''
    api
      .get(`/projects/${projectId}/action-items${q}`)
      .then(res => {
        if (!cancelled) setItems(res.data)
      })
      .catch(err => {
        if (!cancelled) console.error(err)
      })

    return () => {
      cancelled = true
    }
  }, [projectId, filterType])

  const addItem = async () => {
    const title = prompt('Título da ação:')
    if (!title) return
    const type = prompt("Tipo ('Ação Pontual', 'Pendência', 'Chamado', 'Bug'):", "Ação Pontual")
    await api.post(`/projects/${projectId}/action-items`, { title, type, status: 'open' })
    fetchItems()
  }

  return (
    <div>
      <div style={{display: 'flex', gap: 8, alignItems: 'center'}}>
        <button onClick={addItem}>+ Nova Ação</button>
        <select value={filterType} onChange={e => setFilterType(e.target.value)}>
          <option value="">Todos os tipos</option>
          <option>Ação Pontual</option>
          <option>Pendência</option>
          <option>Chamado</option>
          <option>Bug</option>
        </select>
      </div>
      <ul style={{marginTop: 12}}>
        {items.map(it => (
          <li key={it.id}>
            <strong>{it.title}</strong> <em style={{opacity: 0.7}}>({it.type})</em>
          </li>
        ))}
      </ul>
    </div>
  )
}
