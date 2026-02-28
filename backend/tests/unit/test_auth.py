"""
Testes de autenticação
"""
import pytest


def test_register(client):
    """Testa registro de usuário"""
    response = client.post("/api/v1/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"


def test_register_duplicate_email(client, test_user):
    """Testa registro com email duplicado"""
    response = client.post("/api/v1/auth/register", json={
        "name": "Test User 2",
        "email": "test@example.com",
        "password": "test123",
    })
    assert response.status_code == 400


def test_login(client, test_user):
    """Testa login de usuário"""
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "test123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data


def test_login_invalid_credentials(client):
    """Testa login com credenciais inválidas"""
    response = client.post("/api/v1/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrong123",
    })
    assert response.status_code == 401


def test_get_me(client, test_user, auth_headers):
    """Testa obter dados do usuário logado"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_get_me_unauthorized(client):
    """Testa obter dados sem autenticação"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
