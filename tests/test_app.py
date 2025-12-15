import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture que crea un cliente de pruebas para la aplicación Flask.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_app_inicia_correctamente():
    """
    Verifica que la aplicación Flask se crea correctamente.
    """
    assert app is not None


def test_ruta_principal_responde_200(client):
    """
    Verifica que la ruta '/' responde con código HTTP 200.
    """
    response = client.get('/')
    assert response.status_code == 200


def test_lista_tareas_se_muestra_correctamente(client):
    """
    Verifica que la página principal contiene el texto esperado
    relacionado con la lista de tareas.
    """
    response = client.get('/')
    contenido = response.data.decode('utf-8')

    # Título principal de la aplicación
    assert 'Gestor de Tareas' in contenido

    # Estructura básica de la lista
    assert '<ul' in contenido
    assert '</ul>' in contenido
