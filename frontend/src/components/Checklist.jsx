import React, { useEffect, useState } from 'react'
import api from '../api/client'

export default function Checklist({ projectId }) {
  const [groups, setGroups] = useState([])
  const [newGroup, setNewGroup] = useState('')
  const [items, setItems] = useState({})

  const fetchGroups = () => {
    api.get(`/projects/${projectId}/checklist-groups`).then(res => setGroups(res.data))
  }

  useEffect(() => {
    fetchGroups()
  }, [projectId])

  const addGroup = async () => {
    if (!newGroup.trim()) return
    await api.post(`/projects/${projectId}/checklist-groups`, { name: newGroup })
    setNewGroup('')
    fetchGroups()
  }

  const addItem = async (groupId) => {
    const title = prompt('Título do item:')
    if (!title) return
    const type = window.confirm('É documentação? OK=Sim / Cancel=Não') ? 'Documentação' : 'Ação'
    await api.post(`/checklist-groups/${groupId}/items`, { title, type, notes: '' })
    fetchGroups()
  }

  return (
    <div>
      <div style={{display: 'flex', gap: 8}}>
        <input value={newGroup} onChange={e => setNewGroup(e.target.value)} placeholder="Novo grupo" />
        <button onClick={addGroup}>Adicionar Grupo</button>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 12, marginTop: 12}}>
        {groups.map(g => (
          <div key={g.id} style={{border: '1px solid #ddd', borderRadius: 8, padding: 12}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <strong>{g.name}</strong>
              <button onClick={() => addItem(g.id)}>+ Item</button>
            </div>
            {/* Items could be listed via a dedicated endpoint; for MVP, keep minimal */}
            <div style={{opacity: 0.7, fontSize: 12, marginTop: 8}}>Itens aparecem após adicionar (futuro: listagem por grupo)</div>
          </div>
        ))}
      </div>
    </div>
  )
}
