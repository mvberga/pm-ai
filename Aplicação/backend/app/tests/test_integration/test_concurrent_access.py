"""
🧪 Teste de Integração: Acesso Concorrente

Este teste valida o comportamento do sistema com múltiplos usuários acessando simultaneamente:
1. Múltiplos usuários criando projetos
2. Acesso simultâneo aos mesmos recursos
3. Validação de integridade dos dados
4. Performance sob carga
"""

import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.project import Project


@pytest.mark.asyncio
async def test_multiple_users_creating_projects(
    client: AsyncClient,
    db_session: AsyncSession
):
    """
    🎯 Teste: Múltiplos usuários criando projetos simultaneamente
    """
    
    # 1. Criar múltiplos usuários
    users_data = [
        {"email": "user1@example.com", "name": "User 1"},
        {"email": "user2@example.com", "name": "User 2"},
        {"email": "user3@example.com", "name": "User 3"},
        {"email": "user4@example.com", "name": "User 4"},
        {"email": "user5@example.com", "name": "User 5"}
    ]
    
    created_users = []
    for user_data in users_data:
        from app.utils.auth import hash_password
        user = User(
            email=user_data["email"],
            name=user_data["name"],
            hashed_password=hash_password("testpassword")
        )
        db_session.add(user)
        created_users.append(user)
    
    await db_session.commit()
    
    for user in created_users:
        await db_session.refresh(user)
    
    print(f"[OK] {len(created_users)} usuários criados")
    
    # 2. Função para criar projeto
    async def create_project_for_user(user: User, project_number: int):
        project_data = {
            "name": f"Projeto {project_number} - {user.name}",
            "description": f"Projeto de teste para {user.name}",
            "municipio": "São Paulo",  # [OK] NOVO: campo obrigatório
            "entidade": "Prefeitura",  # [OK] NOVO: campo obrigatório
            "portfolio": f"Portfolio {project_number}",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",  # [OK] NOVO: campo obrigatório
            "data_inicio": "2024-01-01",  # [OK] NOVO: campo obrigatório
            "data_fim": "2024-12-31",  # [OK] NOVO: campo obrigatório
            "gerente_projeto_id": 1,  # [OK] NOVO: campo obrigatório
            "gerente_portfolio_id": 1  # [OK] NOVO: campo obrigatório
        }
        
        response = await client.post(
            "/api/v1/projects",
            json=project_data,
            headers={"Authorization": f"Bearer mock_token_{user.id}"}
        )
        
        return response, user.id, project_number
    
    # 3. Criar projetos simultaneamente
    tasks = []
    for i, user in enumerate(created_users):
        task = create_project_for_user(user, i + 1)
        tasks.append(task)
    
    print(f"🚀 Iniciando criação simultânea de {len(tasks)} projetos...")
    
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = asyncio.get_event_loop().time()
    
    execution_time = end_time - start_time
    print(f"[TIME] Tempo de execução: {execution_time:.2f} segundos")
    
    # 4. Verificar resultados
    successful_creations = 0
    failed_creations = 0
    
    for result in results:
        if isinstance(result, Exception):
            failed_creations += 1
            print(f"[ERROR] Falha na criação: {result}")
        else:
            response, user_id, project_number = result
            if response.status_code in [200, 201]:
                successful_creations += 1
                print(f"[OK] Projeto {project_number} criado para usuário {user_id}")
            else:
                failed_creations += 1
                print(f"[ERROR] Falha na criação do projeto {project_number}: {response.status_code}")
    
    print(f"📊 Resultados: {successful_creations} sucessos, {failed_creations} falhas")
    
    # 5. Verificar no banco
    projects_query = select(Project)
    projects_result = await db_session.execute(projects_query)
    all_projects = projects_result.scalars().all()
    
    print(f"📊 Total de projetos no banco: {len(all_projects)}")
    
    # 6. Validar integridade
    assert successful_creations > 0, "Pelo menos um projeto deveria ser criado"
    assert len(all_projects) == successful_creations, "Número de projetos deve corresponder aos criados com sucesso"
    
    print(f"[OK] Teste de criação simultânea concluído com sucesso!")


@pytest.mark.asyncio
async def test_concurrent_project_access(
    client: AsyncClient,
    db_session: AsyncSession
):
    """
    🎯 Teste: Acesso simultâneo aos mesmos projetos
    """
    
    # 1. Criar usuário e projeto
    from app.utils.auth import hash_password
    user = User(
        email="concurrent@example.com",
        name="Concurrent User",
        hashed_password=hash_password("testpassword")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    project_response = await client.post(
        "/api/v1/projects",
        json={
            "name": "Projeto Concorrente",
            "description": "Projeto para teste de acesso simultâneo",
            "municipio": "São Paulo",  # [OK] NOVO: campo obrigatório
            "entidade": "Prefeitura",  # [OK] NOVO: campo obrigatório
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",  # [OK] NOVO: campo obrigatório
            "data_inicio": "2024-01-01",  # [OK] NOVO: campo obrigatório
            "data_fim": "2024-12-31",  # [OK] NOVO: campo obrigatório
            "gerente_projeto_id": 1,  # [OK] NOVO: campo obrigatório
            "gerente_portfolio_id": 1  # [OK] NOVO: campo obrigatório
        },
        headers={"Authorization": f"Bearer mock_token_{user.id}"}
    )
    project_id = project_response.json()["id"]
    
    print(f"[OK] Projeto criado: {project_id}")
    
    # 2. Função para acessar o projeto
    async def access_project(access_number: int):
        response = await client.get(
            f"/api/v1/projects/{project_id}",
            headers={"Authorization": f"Bearer mock_token_{user.id}"}
        )
        return response, access_number
    
    # 3. Acessar o projeto simultaneamente
    tasks = [access_project(i + 1) for i in range(10)]
    
    print(f"🚀 Iniciando 10 acessos simultâneos ao projeto {project_id}...")
    
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = asyncio.get_event_loop().time()
    
    execution_time = end_time - start_time
    print(f"[TIME] Tempo de execução: {execution_time:.2f} segundos")
    
    # 4. Verificar resultados
    successful_accesses = 0
    failed_accesses = 0
    
    for result in results:
        if isinstance(result, Exception):
            failed_accesses += 1
            print(f"[ERROR] Falha no acesso: {result}")
        else:
            response, access_number = result
            if response.status_code == 200:
                successful_accesses += 1
                project_data = response.json()
                print(f"[OK] Acesso {access_number}: Projeto {project_data['name']}")
            else:
                failed_accesses += 1
                print(f"[ERROR] Falha no acesso {access_number}: {response.status_code}")
    
    print(f"📊 Resultados: {successful_accesses} acessos bem-sucedidos, {failed_accesses} falhas")
    
    # 5. Validar integridade
    assert successful_accesses == 10, "Todos os 10 acessos deveriam ser bem-sucedidos"
    assert failed_accesses == 0, "Nenhum acesso deveria falhar"
    
    print(f"[OK] Teste de acesso simultâneo concluído com sucesso!")


@pytest.mark.asyncio
async def test_concurrent_project_updates(
    client: AsyncClient,
    db_session: AsyncSession
):
    """
    🎯 Teste: Atualizações simultâneas do mesmo projeto
    """
    
    # 1. Criar usuário e projeto
    from app.utils.auth import hash_password
    user = User(
        email="update@example.com",
        name="Update User",
        hashed_password=hash_password("testpassword")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    project_response = await client.post(
        "/api/v1/projects",
        json={
            "name": "Projeto para Update",
            "description": "Projeto para teste de atualizações simultâneas",
            "municipio": "São Paulo",  # [OK] NOVO: campo obrigatório
            "entidade": "Prefeitura",  # [OK] NOVO: campo obrigatório
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",  # [OK] NOVO: campo obrigatório
            "data_inicio": "2024-01-01",  # [OK] NOVO: campo obrigatório
            "data_fim": "2024-12-31",  # [OK] NOVO: campo obrigatório
            "gerente_projeto_id": 1,  # [OK] NOVO: campo obrigatório
            "gerente_portfolio_id": 1  # [OK] NOVO: campo obrigatório
        },
        headers={"Authorization": f"Bearer mock_token_{user.id}"}
    )
    project_id = project_response.json()["id"]
    
    print(f"[OK] Projeto criado: {project_id}")
    
    # 2. Função para atualizar o projeto
    async def update_project(update_number: int):
        update_data = {
            "name": f"Projeto Atualizado {update_number}",
            "description": f"Descrição atualizada {update_number}",
            "portfolio": f"Portfolio {update_number}",
            "vertical": "Technology",
            "product": "Software"
        }
        
        response = await client.put(
            f"/api/v1/projects/{project_id}",
            json=update_data,
            headers={"Authorization": f"Bearer mock_token_{user.id}"}
        )
        
        return response, update_number
    
    # 3. Atualizar o projeto simultaneamente
    tasks = [update_project(i + 1) for i in range(5)]
    
    print(f"🚀 Iniciando 5 atualizações simultâneas ao projeto {project_id}...")
    
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = asyncio.get_event_loop().time()
    
    execution_time = end_time - start_time
    print(f"[TIME] Tempo de execução: {execution_time:.2f} segundos")
    
    # 4. Verificar resultados
    successful_updates = 0
    failed_updates = 0
    
    for result in results:
        if isinstance(result, Exception):
            failed_updates += 1
            print(f"[ERROR] Falha na atualização: {result}")
        else:
            response, update_number = result
            if response.status_code == 200:
                successful_updates += 1
                project_data = response.json()
                print(f"[OK] Atualização {update_number}: Projeto {project_data['name']}")
            else:
                failed_updates += 1
                print(f"[ERROR] Falha na atualização {update_number}: {response.status_code}")
    
    print(f"📊 Resultados: {successful_updates} atualizações bem-sucedidas, {failed_updates} falhas")
    
    # 5. Verificar estado final no banco
    project_query = select(Project).where(Project.id == project_id)
    project_result = await db_session.execute(project_query)
    final_project = project_result.scalar_one()
    
    print(f"📊 Estado final do projeto: {final_project.name}")
    
    # 6. Validar integridade
    assert successful_updates > 0, "Pelo menos uma atualização deveria ser bem-sucedida"
    
    print(f"[OK] Teste de atualizações simultâneas concluído com sucesso!")


@pytest.mark.asyncio
async def test_concurrent_database_operations(
    client: AsyncClient,
    db_session: AsyncSession
):
    """
    🎯 Teste: Operações simultâneas no banco de dados
    """
    
    # 1. Criar usuário
    from app.utils.auth import hash_password
    user = User(
        email="db_ops@example.com",
        name="DB Operations User",
        hashed_password=hash_password("testpassword")
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    # 2. Criar projeto
    project_response = await client.post(
        "/api/v1/projects",
        json={
            "name": "Projeto DB Ops",
            "description": "Projeto para teste de operações simultâneas no banco",
            "municipio": "São Paulo",  # [OK] NOVO: campo obrigatório
            "entidade": "Prefeitura",  # [OK] NOVO: campo obrigatório
            "portfolio": "Test Portfolio",
            "vertical": "Technology",
            "product": "Software",
            "tipo": "implantacao",  # [OK] NOVO: campo obrigatório
            "data_inicio": "2024-01-01",  # [OK] NOVO: campo obrigatório
            "data_fim": "2024-12-31",  # [OK] NOVO: campo obrigatório
            "gerente_projeto_id": 1,  # [OK] NOVO: campo obrigatório
            "gerente_portfolio_id": 1  # [OK] NOVO: campo obrigatório
        },
        headers={"Authorization": f"Bearer mock_token_{user.id}"}
    )
    project_id = project_response.json()["id"]
    
    print(f"[OK] Projeto criado: {project_id}")
    
    # 3. Função para operações simultâneas
    async def perform_db_operation(operation_number: int):
        # Simular diferentes operações no banco
        if operation_number % 2 == 0:
            # Operação de leitura
            response = await client.get(
                f"/api/v1/projects/{project_id}",
                headers={"Authorization": f"Bearer mock_token_{user.id}"}
            )
            return response, operation_number, "read"
        else:
            # Operação de atualização
            update_data = {
                "name": f"Projeto Atualizado {operation_number}",
                "description": f"Descrição atualizada {operation_number}",
                "portfolio": f"Portfolio {operation_number}",
                "vertical": "Technology",
                "product": "Software"
            }
            response = await client.put(
                f"/api/v1/projects/{project_id}",
                json=update_data,
                headers={"Authorization": f"Bearer mock_token_{user.id}"}
            )
            return response, operation_number, "update"
    
    # 4. Executar operações simultâneas
    tasks = [perform_db_operation(i + 1) for i in range(8)]
    
    print(f"🚀 Iniciando 8 operações simultâneas no banco...")
    
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = asyncio.get_event_loop().time()
    
    execution_time = end_time - start_time
    print(f"[TIME] Tempo de execução: {execution_time:.2f} segundos")
    
    # 5. Verificar resultados
    successful_operations = 0
    failed_operations = 0
    
    for result in results:
        if isinstance(result, Exception):
            failed_operations += 1
            print(f"[ERROR] Falha na operação: {result}")
        else:
            response, operation_number, operation_type = result
            if response.status_code in [200, 201]:
                successful_operations += 1
                print(f"[OK] Operação {operation_number} ({operation_type}): Sucesso")
            else:
                failed_operations += 1
                print(f"[ERROR] Falha na operação {operation_number} ({operation_type}): {response.status_code}")
    
    print(f"📊 Resultados: {successful_operations} operações bem-sucedidas, {failed_operations} falhas")
    
    # 6. Validar integridade
    assert successful_operations > 0, "Pelo menos uma operação deveria ser bem-sucedida"
    
    print(f"[OK] Teste de operações simultâneas no banco concluído com sucesso!")


@pytest.mark.asyncio
async def test_system_under_load(
    client: AsyncClient,
    db_session: AsyncSession
):
    """
    �� Teste: Sistema sob carga com múltiplas operações
    """
    
    # 1. Criar múltiplos usuários
    users_data = [
        {"email": f"loaduser{i}@example.com", "name": f"Load User {i}"}
        for i in range(1, 11)  # 10 usuários
    ]
    
    created_users = []
    for user_data in users_data:
        from app.utils.auth import hash_password
        user = User(
            email=user_data["email"],
            name=user_data["name"],
            hashed_password=hash_password("testpassword")
        )
        db_session.add(user)
        created_users.append(user)
    
    await db_session.commit()
    
    for user in created_users:
        await db_session.refresh(user)
    
    print(f"[OK] {len(created_users)} usuários criados para teste de carga")
    
    # 2. Função para operação completa
    async def perform_complete_operation(user: User, operation_number: int):
        try:
            # 1. Criar projeto
            project_response = await client.post(
                "/api/v1/projects",
                json={
                    "name": f"Projeto Carga {operation_number}",
                    "description": f"Projeto de teste de carga {operation_number}",
                    "municipio": "São Paulo",  # [OK] NOVO: campo obrigatório
                    "entidade": "Prefeitura",  # [OK] NOVO: campo obrigatório
                    "portfolio": f"Portfolio Carga {operation_number}",
                    "vertical": "Technology",
                    "product": "Software",
                    "tipo": "implantacao",  # [OK] NOVO: campo obrigatório
                    "data_inicio": "2024-01-01",  # [OK] NOVO: campo obrigatório
                    "data_fim": "2024-12-31",  # [OK] NOVO: campo obrigatório
                    "gerente_projeto_id": 1,  # [OK] NOVO: campo obrigatório
                    "gerente_portfolio_id": 1  # [OK] NOVO: campo obrigatório
                },
                headers={"Authorization": f"Bearer mock_token_{user.id}"}
            )
            
            if project_response.status_code not in [200, 201]:
                return f"Falha ao criar projeto: {project_response.status_code}", operation_number
            
            project_id = project_response.json()["id"]
            
            # 2. Criar checklist
            checklist_response = await client.post(
                "/api/v1/checklists",
                json={
                    "name": f"Checklist Carga {operation_number}",
                    "description": f"Checklist de teste de carga {operation_number}",
                    "project_id": project_id
                },
                headers={"Authorization": f"Bearer mock_token_{user.id}"}
            )
            
            if checklist_response.status_code not in [200, 201]:
                return f"Falha ao criar checklist: {checklist_response.status_code}", operation_number
            
            # 3. Criar action item
            action_item_response = await client.post(
                "/api/v1/action-items/",
                json={
                    "title": f"Ação Carga {operation_number}",
                    "description": f"Ação de teste de carga {operation_number}",
                    "type": "action",
                    "priority": "medium",
                    "project_id": project_id
                },
                headers={"Authorization": f"Bearer mock_token_{user.id}"}
            )
            
            if action_item_response.status_code != 201:
                return f"Falha ao criar action item: {action_item_response.status_code}", operation_number
            
            return "Sucesso", operation_number
            
        except Exception as e:
            return f"Exceção: {str(e)}", operation_number
    
    # 3. Executar operações simultâneas
    tasks = []
    for i, user in enumerate(created_users):
        for j in range(3):  # 3 operações por usuário = 30 operações totais
            task = perform_complete_operation(user, f"{i+1}.{j+1}")
            tasks.append(task)
    
    print(f"🚀 Iniciando {len(tasks)} operações simultâneas para teste de carga...")
    
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = asyncio.get_event_loop().time()
    
    execution_time = end_time - start_time
    print(f"[TIME] Tempo total de execução: {execution_time:.2f} segundos")
    print(f"🚀 Taxa: {len(tasks)/execution_time:.2f} operações/segundo")
    
    # 4. Verificar resultados
    successful_operations = 0
    failed_operations = 0
    
    for result in results:
        if isinstance(result, Exception):
            failed_operations += 1
        elif isinstance(result, tuple) and result[0] == "Sucesso":
            successful_operations += 1
        else:
            failed_operations += 1
    
    print(f"📊 Resultados finais: {successful_operations} sucessos, {failed_operations} falhas")
    
    # 5. Validar performance
    assert execution_time < 30, f"Teste de carga deve completar em menos de 30 segundos, levou {execution_time:.2f}s"
    assert successful_operations > len(tasks) * 0.8, f"Taxa de sucesso deve ser >80%, foi {successful_operations/len(tasks)*100:.1f}%"
    
    print(f"[OK] Teste de carga concluído com sucesso!")
    print(f"   🚀 {len(tasks)} operações em {execution_time:.2f}s")
    print(f"   🚀 Taxa: {len(tasks)/execution_time:.2f} ops/s")
    print(f"   [OK] Sucesso: {successful_operations}/{len(tasks)} ({successful_operations/len(tasks)*100:.1f}%)")
