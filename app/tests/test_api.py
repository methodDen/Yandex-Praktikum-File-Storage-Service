from pathlib import Path

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ping_db(
    async_client: AsyncClient,
):
    response = await async_client.get('/health-check/ping')
    assert response.status_code == 200
    assert response.json() == {'message': 'Database is healthy'}


@pytest.mark.asyncio
async def test_create_user(
    async_client: AsyncClient,
):
    payload = {
        "username": "test",
        "password": "testtest",
    }
    response = await async_client.post(
        "/auth/register",
        json=payload,
    )
    assert response.status_code == 201
    json = response.json()
    assert json['username'] == payload['username']
    assert 'password' in json


@pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient,
):
    payload = {
        "username": "test_2",
        "password": "testtest",
    }
    await async_client.post(
        "/auth/register",
        json=payload,
    )

    response = await async_client.post(
        "/auth/token",
        data=payload,
    )
    assert response.status_code == 200
    json = response.json()
    assert 'access_token' in json


@pytest.mark.asyncio
async def test_upload_file(async_client_auth):
    path_of_upload_file = Path('/src/app/tests/test_file.txt')
    file = {'file_to_be_saved': path_of_upload_file.open('rb')}
    response = await async_client_auth.post(
        '/file/upload',
        files=file,
    )
    assert response.status_code == 201
    json = response.json()
    assert json['name'] == path_of_upload_file.name
    assert json['path'] == f'files/{path_of_upload_file.name}'
    assert json['size'] == path_of_upload_file.stat().st_size
    assert 'created_at' in json
    assert 'id' in json
    assert 'user_id' in json


@pytest.mark.asyncio
async def test_download_file(async_client_auth):
    path_of_upload_file = Path('/src/app/tests/test_file.txt')
    file = {'file_to_be_saved': path_of_upload_file.open('rb')}
    response = await async_client_auth.post(
        '/file/upload',
        files=file,
    )
    assert response.status_code == 201
    json = response.json()
    assert json['name'] == path_of_upload_file.name
    assert json['path'] == f'files/{path_of_upload_file.name}'
    assert json['size'] == path_of_upload_file.stat().st_size
    assert 'created_at' in json
    assert 'id' in json
    assert 'user_id' in json

    response = await async_client_auth.get(
        '/file/download',
        params={
            'path': f'files/{path_of_upload_file.name}'
        }
    )
    assert response.status_code == 200
    assert response.content == path_of_upload_file.read_bytes()


@pytest.mark.asyncio
async def test_list_files(async_client_auth):
    path_of_upload_file = Path('/src/app/tests/test_file.txt')
    file = {'file_to_be_saved': path_of_upload_file.open('rb')}
    response = await async_client_auth.post(
        '/file/upload',
        files=file,
    )
    assert response.status_code == 201
    json = response.json()
    assert json['name'] == path_of_upload_file.name
    assert json['path'] == f'files/{path_of_upload_file.name}'
    assert json['size'] == path_of_upload_file.stat().st_size
    assert 'created_at' in json
    assert 'id' in json
    assert 'user_id' in json

    response = await async_client_auth.get(
        '/file/list',
        params={
            'path': f'files/{path_of_upload_file.name}'
        }
    )
    assert response.status_code == 200
    json = response.json()
    assert json['files'][0]['name'] == path_of_upload_file.name
    assert json['files'][0]['path'] == f'files/{path_of_upload_file.name}'
    assert json['files'][0]['size'] == path_of_upload_file.stat().st_size
    assert 'created_at' in json['files'][0]
    assert 'id' in json['files'][0]
    assert 'user_id' in json['files'][0]