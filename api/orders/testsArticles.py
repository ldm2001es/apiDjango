import logging
import os
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse
from datetime import datetime

if os.path.exists('logs/testsArticles.log'):
    os.remove('logs/testsArticles.log')
logging.basicConfig(filename='logs/testsArticles.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ArticlesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        try:
            if os.path.exists('logs/testsArticles.log'):
                os.remove('logs/testsArticles.log')
        except:
            pass
        User.objects.create_user(username='admin', password='admin')
        cls.logger = logging.getLogger(__name__)  
         # Create a file handler
        handler = logging.FileHandler('logs/testsArticles.log')

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        cls.logger.setLevel(logging.INFO)
        cls.logger.addHandler(handler)

    @classmethod
    def tearDownClass(cls):
        # Close the file handlers of the logger
        for handler in cls.logger.handlers:
            handler.close()
            cls.logger.removeHandler(handler)
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='admin', password='admin')
        self.id = 0        

    def tearDown(self):
        if (self.id != 0):
            response = self.client.delete('/articles/' + str(self.id) + '/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_articles(self):        
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data =  []
        self.assertEqual(response.data, expected_data)
        # A new register is added
        new_article = {'reference':'1', 'name':'1', 'description':'1', 'price':'1', 'tax':'1'}
        response = self.client.post('/articles/', new_article, format='json')
        self.id = response.data['id']
        # Retrieve all articles
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info('Get Articles - Response data: %s', response.data)
        self.assertEqual(len(response.data), 1)
        
    def test_post_article(self):
        new_article = {'reference':'1', 'name':'1', 'description':'1', 'price':'1', 'tax':'1'}
        response = self.client.post('/articles/', new_article, format='json')
        self.id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logger.info('Post Article - Response data: %s', response.data)
        expected_data = {'id': self.id, 
                         'url': 'http://testserver/articles/' + str(self.id) + '/', 
                         'reference': '1', 'name': '1', 
                         'description': '1', 
                         'price': 1.0, 'tax': 1.0, 
                         'creation_date': datetime.now().date().strftime('%Y-%m-%d')
        }
        self.logger.info('Post Article - Expected data: %s', expected_data)
        self.assertEqual(response.data, expected_data)

    def test_put_article(self):
        new_article = {'reference':'1', 'name':'1', 'description':'1', 'price':'1', 'tax':'1'}
        response = self.client.post('/articles/', new_article, format='json')
        self.id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logger.info('Post Article - Response data: %s', response.data)
        expected_data = {'id': self.id, 
                         'url': 'http://testserver/articles/' + str(self.id) + '/', 
                         'reference': '1', 'name': '1', 
                         'description': '1', 
                         'price': 1.0, 'tax': 1.0, 
                         'creation_date': datetime.now().date().strftime('%Y-%m-%d')
        }        
        self.assertEqual(response.data, expected_data)
        response = self.client.put('/articles/' + str(self.id) + '/', {'reference':'2', 'name':'2', 'description':'2', 'price':'2', 'tax':'2'}, format='json')
        expected_data = {'id': self.id, 
                         'url': 'http://testserver/articles/' + str(self.id) + '/', 
                         'reference': '2', 'name': '2', 
                         'description': '2', 
                         'price': 2.0, 'tax': 2.0, 
                         'creation_date': datetime.now().date().strftime('%Y-%m-%d')
        }
        self.assertEqual(response.data, expected_data)
        self.logger.info('Post Article - Expected data: %s', expected_data)

    def test_delete_article(self):
        new_article = {'reference':'1', 'name':'1', 'description':'1', 'price':'1', 'tax':'1'}
        response = self.client.post('/articles/', new_article, format='json')
        new_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)                
        response = self.client.get('/articles/' + str(new_id), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info('Delete - Create Article - Response data: %s', response.data)        
        self.logger.info('Delete Article: %s', response.data['id'])
        response = self.client.delete('/articles/' + str(new_id) + '/')
        self.logger.info('Delete Article Response: %s', response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/articles/' + str(new_id), follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_article(self):
        new_article = {'reference':'1', 'name':'1', 'description':'1', 'price':'1', 'tax':'1'}
        response = self.client.post('/articles/', new_article, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logger.info('Get Article - Response data: %s', response.data)
        self.id = response.data['id']
        response = self.client.get('/articles/' + str(self.id), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info('Get Article by Id - Response data: %s', response.data)
        expected_data = {'id': self.id, 'url': 'http://testserver/articles/' + str(self.id) + '/', 'reference': '1', 'name': '1', 'description': '1', 'price': 1.0, 'tax': 1.0, 'creation_date': datetime.now().date().strftime('%Y-%m-%d')}
        self.assertEqual(response.data, expected_data)
