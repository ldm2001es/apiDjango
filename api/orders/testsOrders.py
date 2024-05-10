import logging
import os
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
from .models import Article

class OrdersTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        if os.path.exists('logs/testsOrders.log'):
            os.remove('logs/testsOrders.log')
        User.objects.create_user(username='admin', password='admin')
        cls.logger = logging.getLogger(__name__)  
         # Create a file handler
        handler = logging.FileHandler('logs/testsOrders.log')

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
            response = self.client.delete('/orders/' + str(self.id) + '/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def _test_get_all(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info('Get Orders - Response data: %s', response.data)
        expected_data =  [] 
        self.assertEqual(response.data, expected_data)
        # A new order is added
        new_article = { "articles": [{"reference": "1", "amount": "77"}]}
        response = self.client.post('/orders/', new_article, format='json')
        self.logger.info('Get Orders - Response data: %s', response.data)
        self.id = response.data['id']
        # Retrieve all orders
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info('Get Orders - Response data: %s', response.data)
        self.assertEqual(len(response.data), 1)
        return response

    def _test_post(self, new_register):        
        response = self.client.post('/orders/', new_register, format='json')
        self.id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response
    
    def _test_get_register(self):
        new_register = { "articles": [{"reference": "1", "amount": "77"}]}
        response = self.client.post('/orders/', new_register, format='json')
        self.id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.logger.info('Get Register by Id - Response data: %s', response.data)
        self.id = response.data['id']
        response = self.client.get('/orders/' + str(self.id), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response    
    
    def _test_put(self):
        new_register = { "articles": [{"reference": "1", "amount": "77"}]}
        response = self.client.post('/orders/', new_register, format='json')       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.id = response.data['id']
        response = self.client.put('/orders/' + str(self.id) + '/', { "articles": [{"reference": "1", "amount": "99"}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response
    
    def test_get_all(self):      
        response = self._test_get_all()  
        self.assertEqual(len(response.data[0]["articles"]), 0)

    def test_get_all_with_article(self):       
        article = Article.objects.create(reference='1', name='1', description=1, price=1, tax=1, creation_date=datetime.now().date())    
        response = self._test_get_all()  
        self.assertEqual(len(response.data[0]["articles"]), 1)
        Article.objects.all().delete()

    def test_post_only_article(self):
        new_register = { "articles": [{"reference": "1", "amount": "77"}]}
        response = self._test_post(new_register)  
        self.assertEqual(len(response.data["articles"]), 0)   
        self.assertEqual(response.data["price"], 0) 
        self.assertEqual(response.data["tax_price"], 0)    
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))   

    def test_post_with_data(self):
        new_register = { "articles": [{"reference": "1", "amount": "77"}], "price": 10, "tax_price": 10, "creation_date": "2020-10-10"}
        response = self._test_post(new_register)  
        self.assertEqual(len(response.data["articles"]), 0)   
        self.assertEqual(response.data["price"], 0) 
        self.assertEqual(response.data["tax_price"], 0)    
        self.assertEqual(response.data["creation_date"], "2020-10-10")   

    def test_post_with_article(self):
        article = Article.objects.create(reference='1', name='1', description=1, price=1, tax=1, creation_date=datetime.now().date())
        new_register = { "articles": [{"reference": "1", "amount": "77"}]}   
        response = self._test_post(new_register) 
        self.assertEqual(len(response.data["articles"]), 1)
        self.assertEqual(response.data["price"], 77) 
        self.assertEqual(response.data["tax_price"], 77.77) 
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))   
        Article.objects.all().delete() 
    
    def test_put(self):
        response = self._test_put()  
        self.assertEqual(len(response.data["articles"]), 0)   
        self.assertEqual(response.data["price"], 0) 
        self.assertEqual(response.data["tax_price"], 0)    
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))    
    
    def test_put_with_new_article(self):
        Article.objects.create(reference='1', name='1', description=1, price=1, tax=1, creation_date=datetime.now().date())           
        response = self._test_put()  
        self.assertEqual(len(response.data["articles"]), 1)   
        self.assertEqual(response.data["price"], 99) 
        self.assertEqual(response.data["tax_price"], 99.99)
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))     
        Article.objects.all().delete() 

    def test_put_with_new_and_old_article(self):
        Article.objects.create(reference='1', name='1', description=1, price=1, tax=1, creation_date=datetime.now().date())           
        Article.objects.create(reference='2', name='2', description=2, price=2, tax=2, creation_date=datetime.now().date())           
        new_register = { "articles": [{"reference": "1", "amount": "77"}]}
        response = self.client.post('/orders/', new_register, format='json')       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.id = response.data['id']
        order_article = response.data['articles'][0]
        order_article['amount'] = 66
        
        response = self.client.put('/orders/' + str(self.id) + '/', { "articles": [order_article, {"reference": "2", "amount": "22"}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["articles"]), 2)   
        self.assertEqual(response.data["price"], 110) 
        self.assertEqual(response.data["tax_price"], 111.53999999999999)
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))     
        Article.objects.all().delete() 

    def test_delete_order(self):
        new_register = { "articles": [{"reference": "1", "amount": "77"}]}
        response = self.client.post('/orders/', new_register, format='json') 
        new_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)                
        response = self.client.get('/orders/' + str(new_id), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info('Delete - Create Article - Response data: %s', response.data)        
        self.logger.info('Delete Article: %s', response.data['id'])
        response = self.client.delete('/orders/' + str(new_id) + '/')
        self.logger.info('Delete Article Response: %s', response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/orders/' + str(new_id), follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_register(self):
        response = self._test_get_register()  
        self.assertEqual(len(response.data["articles"]), 0)  
        self.assertEqual(response.data["price"], 0) 
        self.assertEqual(response.data["tax_price"], 0) 
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))   
    
    def test_get_register_with_article(self):
        article = Article.objects.create(reference='1', name='1', description=1, price=1, tax=1, creation_date=datetime.now().date())   
        response = self._test_get_register()  
        self.assertEqual(len(response.data["articles"]), 1)
        self.assertEqual(response.data["price"], 77) 
        self.assertEqual(response.data["tax_price"], 77.77)
        self.assertEqual(response.data["creation_date"], datetime.now().date().strftime('%Y-%m-%d'))   
        Article.objects.all().delete()  
