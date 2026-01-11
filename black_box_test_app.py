import pytest
from app import app  # Assuming your Flask app is in app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_upload_valid_files(client):
    with open('test_orders.csv', 'rb') as orders, open('test_inventory.csv', 'rb') as inventory, open('test_sfc.csv', 'rb') as sfc:
        response = client.post('/upload', data={
            'Orders': orders,
            'Inventory': inventory,
            'SFC': sfc
        })
    assert response.status_code == 200
    assert 'inventory_level' in response.json

# Additional tests would go here for each test case...

