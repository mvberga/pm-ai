# Projeto: Sistema de Gestão de Projetos (Gantt • Kanban • Timeline)

## 📌 Solicitação do Usuário

O objetivo é criar o layout de um sistema baseado na **gestão de
projetos**, contendo:

-   **Gantt** para visualização de cronogramas.
-   **Kanban** para gestão de fluxo de tarefas.
-   **Timeline contínua** para exibir o histórico do projeto.
-   Marcos dinâmicos na timeline (expansão ao clique ou hover).
-   **Filtros dinâmicos** aplicados à timeline (datas, períodos,
    contexto, palavras‑chave).

A stack definida pelo usuário foi: - **Frontend:** React (Vite)\
- **Backend:** Python (FastAPI)\
- **Banco de Dados:** PostgreSQL (com pgvector)\
- **Automação:** n8n\
- **Hospedagem:** Docker em VM\
- **UI Libraries sugeridas:** Frappe Gantt, SortableJS

------------------------------------------------------------------------

## 🤖 Racional do Retorno

Com base na solicitação, foram sugeridos:

1.  **Bibliotecas OSS/gratuitas**
    -   **Gantt:** Frappe Gantt, gantt-task-react, jsGanttImproved,
        DayPilot Lite.\
    -   **Kanban:** @hello-pangea/dnd, dnd-kit, jKanban, SortableJS.\
    -   **Timeline:** vis-timeline (com filtros por Fuse.js e date-fns).
2.  **UI/UX**
    -   Uso de **Tailwind + shadcn/ui** para consistência de design.
    -   **Drawer lateral** para exibir detalhes dos marcos.
    -   **Painel de filtros** persistente, integrado ao n8n para salvar
        preferências.
3.  **Implementação React**
    -   Estrutura com tabs **Gantt / Kanban / Timeline**.
    -   Filtros dinâmicos (texto, datas, contexto).
    -   Timeline interativa com hover e clique.
    -   Kanban com drag & drop.
    -   Gantt renderizado dinamicamente via `frappe-gantt`.

------------------------------------------------------------------------

## 🧩 Código Proposto (React + Tailwind + shadcn/ui)

``` tsx
// App.tsx (resumido)
import React, { useState, useMemo } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";

// Dados mock
const SAMPLE = [{ id: "1", title: "Kickoff", start: "2025-08-05", status: "done", context: ["Meeting"] }];

// Filtros
const DEFAULT_FILTERS = { query: "", contexts: [] };

export default function App() {
  const [active, setActive] = useState("Timeline");
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [data, setData] = useState(SAMPLE);
  const filtered = useMemo(() => data, [data, filters]);

  return (
    <div className="h-screen w-full bg-gray-50">
      <header className="border-b p-3 flex gap-4">
        <div className="font-semibold">PM Suite</div>
        {["Gantt", "Kanban", "Timeline"].map(t => (
          <button key={t} onClick={() => setActive(t)}>{t}</button>
        ))}
      </header>

      <main className="flex gap-4 p-4">
        <aside className="w-[320px] border-r p-4">Painel de filtros...</aside>
        <section className="flex-1 border p-4">
          {active === "Gantt" && <div>📊 Gantt (Frappe)</div>}
          {active === "Kanban" && <div>📋 Kanban (Drag & Drop)</div>}
          {active === "Timeline" && <div>⏳ Timeline (vis-timeline)</div>}
        </section>
      </main>
    </div>
  );
}
```

> O código completo (com Drawer, filtros e integrações dinâmicas) foi
> entregue no esqueleto inicial em React no canvas.

------------------------------------------------------------------------

## ✅ Próximos Passos

-   Implementar backend com FastAPI para persistência de filtros e
    itens.\
-   Conectar com PostgreSQL para histórico + vetores de busca
    semântica.\
-   Orquestrar integrações e notificações via **n8n**.\
-   Refinar UX com **shadcn/ui** (popover, dialog, chips de filtro).
