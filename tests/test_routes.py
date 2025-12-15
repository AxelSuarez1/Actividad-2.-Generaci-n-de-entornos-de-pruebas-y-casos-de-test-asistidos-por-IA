import pytest
import sqlite3
import uuid
from app import app, DATABASE


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def obtener_ultimo_id():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tareas ORDER BY id DESC LIMIT 1")
    tarea_id = cursor.fetchone()[0]
    conn.close()
    return tarea_id


def test_crear_tarea_post(client):
    titulo = f"Tarea integración {uuid.uuid4()}"

    response = client.post(
        '/agregar',
        data={'titulo': titulo},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert titulo in response.data.decode('utf-8')


def test_eliminar_tarea(client):
    titulo = f"Tarea a eliminar {uuid.uuid4()}"

    # Crear tarea
    client.post(
        '/agregar',
        data={'titulo': titulo},
        follow_redirects=True
    )

    # Confirmar que existe
    response_listado = client.get('/')
    assert titulo in response_listado.data.decode('utf-8')

    # Obtener ID real
    tarea_id = obtener_ultimo_id()

    # Eliminar tarea
    client.get(f'/eliminar/{tarea_id}', follow_redirects=True)

    response_final = client.get('/')
    assert titulo not in response_final.data.decode('utf-8')


def test_cambios_reflejados_en_respuesta(client):
    titulo = f"Tarea visible {uuid.uuid4()}"

    # Crear tarea
    client.post(
        '/agregar',
        data={'titulo': titulo},
        follow_redirects=True
    )

    response_crear = client.get('/')
    assert titulo in response_crear.data.decode('utf-8')

    # Eliminar tarea
    tarea_id = obtener_ultimo_id()
    client.get(f'/eliminar/{tarea_id}', follow_redirects=True)

    response_final = client.get('/')
    assert titulo not in response_final.data.decode('utf-8')
