import unittest
import json
import os
from app import app, db, User

class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db = db

        # Cria tabelas no banco de dados para os testes
        with app.app_context():
            self.db.create_all()

    def tearDown(self):
        # Limpa as tabelas após os testes
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_create_user(self):
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "phone": "123456789",
            "address": "123 Test St",
            "is_admin": False
        }

        response = self.app.post('/users', json=user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)  # Verifica se o usuário foi criado com sucesso
        self.assertEqual(data['data']['user']['name'], user_data['name'])  # Verifica se os dados do usuário coincidem

    def test_update_user(self):
        new_user_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "password456",
            "phone": "0987654321",
            "address": "456 Avenue",
            "is_admin": True
        }
        response = self.app.post('/users', json=new_user_data)
        user_id = response.json['data']['user']['id']

        updated_user_data = {
            "name": "Jane Updated",
            "email": "jane_updated@example.com",
            "password": "updatedpassword789",
            "phone": "1357924680",
            "address": "789 Road",
            "is_admin": False
        }
        response = self.app.put(f'/users/{user_id}', json=updated_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json['data'])
        self.assertEqual(response.json['data']['user']['name'], updated_user_data['name'])
    
    def test_update_all_users(self):
        # preservar os dados antigos antes de limpar a tabela
        old_users = self.app.get('/users').json['data']['users']
        # Limpar a tabela de usuários antes de iniciar os testes
        response = self.app.delete('/users')

        # Dados do novo usuário a ser criado
        new_user_data = [
            {
                "name": "Test User",
                "email": "test@example.com",
                "password": "password",
                "phone": "1234567890",
                "address": "123 Test St",
                "is_admin": False
            }
        ]
        # Envia a requisição POST para criar o usuário
        response = self.app.put('/users', data=json.dumps(new_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Verifica se a requisição foi bem-sucedida

        # Obtém todos os usuários após a criação
        response = self.app.get('/users')
        data = json.loads(response.data.decode())

        # Verifica se o novo usuário está na lista de usuários retornados
        self.assertEqual(len(data['data']['users']), 1)
        self.assertEqual(data['data']['users'][0]['email'], 'test@example.com')

        # Restaura os dados antigos da tabela de usuários
        for user in old_users:
            response = self.app.post('/users', json=user)
            self.assertEqual(response.status_code, 201)


    def test_delete_user(self):
        new_user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
            "phone": "9876543210",
            "address": "789 Lane",
            "is_admin": False
        }
        response = self.app.post('/users', json=new_user_data)
        user_id = response.json['data']['user']['id']

        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json['data'])

    def test_delete_all_users(self):
        response = self.app.delete('/users')
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        elif response.status_code == 404:
            self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['data']['users'], [])
    
    def test_get_all_users(self):
        response = self.app.get('/users')
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        elif response.status_code == 404:
            self.assertEqual(response.status_code, 404)
        self.assertIn('users', response.json['data'])
    
    def test_get_user_by_id(self):
        test_user = User(name="Test User", email="test@example.com", password="testpass", phone="123456789", address="Test Address", is_admin=False)
        response = self.app.post('/users', json=test_user.json())
        if response.status_code == 201:
            response = self.app.get(f'/users/name/{test_user.name}')
            new_user_id = response.json['data']['user'][0]['id']
            response = self.app.get(f'/users/{new_user_id}')
            self.assertEqual(response.status_code, 200)
            user_details = json.loads(response.data)['data']['user']
            self.assertEqual(user_details['name'], test_user.name)
            self.assertEqual(user_details['email'], test_user.email)
    
    def test_get_admin_users(self):
        admin_user = User(name="Admin User", email="admin@example.com", password="adminpass", phone="987654321", address="Admin Address", is_admin=True)
        response = self.app.post('/users', json=admin_user.json())
        non_admin_user = User(name="Regular User", email="regular@example.com", password="regularpass", phone="456123789", address="Regular Address", is_admin=False)
        response = self.app.post('/users', json=non_admin_user.json())
        
        response = self.app.get('/users/admin')
        self.assertEqual(response.status_code, 200)

        admin_users = json.loads(response.data)['data']['users']
        self.assertEqual(len(admin_users), 1)
        self.assertEqual(admin_users[0]['name'], admin_user.name)
    
    def test_get_users_by_name(self):
        user1 = User(name="John Doe", email="john@example.com", password="johnpass", phone="123456789", address="John's Address", is_admin=False)
        response = self.app.post('/users', json=user1.json())
        user2 = User(name="Jane Smith", email="jane@example.com", password="janepass", phone="987654321", address="Jane's Address", is_admin=False)
        response = self.app.post('/users', json=user2.json())
        user3 = User(name="John Smith", email="john_smith@example.com", password="johnsmithpass", phone="456123789", address="John Smith's Address", is_admin=False)
        response = self.app.post('/users', json=user3.json())
        user4 = User(name="John Doe", email="john_doe@example.com", password="johndoepass", phone="1357924680", address="John Doe's Address", is_admin=False)
        response = self.app.post('/users', json=user4.json())
        user5 = User(name="John Doe", email="john_doe2@example.com", password="johndoepass2", phone="1357924680", address="John Doe's Address", is_admin=False)
        response = self.app.post('/users', json=user5.json())
                     
        response = self.app.get('/users/name/John')
        self.assertEqual(response.status_code, 200)

        users_with_name = json.loads(response.data)['data']['user']
        self.assertGreaterEqual(len(users_with_name), 1)
        self.assertEqual(users_with_name[0]['name'], user1.name)


if __name__ == '__main__':
    unittest.main()