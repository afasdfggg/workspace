import random
import string
from typing import Dict

from fastapi.testclient import TestClient


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_admin_token_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    login_data = {
        "username": email,
        "password": password,
    }
    r = client.post("/api/v1/auth/admin/login", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_employee_token_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    login_data = {
        "username": email,
        "password": password,
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers