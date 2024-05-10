from django.contrib.auth.models import Group, User
from .models import Article, Order, Order_Article
from rest_framework import serializers
import logging

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    creation_date = serializers.DateField(required=False)
    class Meta:
        model = Article
        fields = ['id', 'url', 'reference', 'name', 'description', 'price', 'tax', 'creation_date']

class Order_ArticleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    reference = serializers.CharField(write_only=True, required=False)
    article = ArticleSerializer(required=False)
    
    class Meta:
        model = Order_Article
        fields = ['id', 'amount', 'reference', 'article']

    def create(self, validated_data):
        logger.info("context data %s" % self.context['request'].data)                
        reference = self.context['request'].data.get('reference')

        if reference is not None:
            try:
                article = Article.objects.get(reference=reference)
            except Article.DoesNotExist:
                raise serializers.ValidationError("Article with this reference does not exist.")

        validated_data.pop('article', None)

        order_article = super().create(validated_data)

        order_article.article = article
        order_article.save()

        return order_article

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    creation_date = serializers.DateField(required=False, allow_null=True)
    price = serializers.FloatField(required=False, allow_null=True)
    tax_price = serializers.FloatField(required=False, allow_null=True)
    articles = Order_ArticleSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'price', 'tax_price', 'articles', 'creation_date']

    @staticmethod
    def _common_articles(list1, list2):
        list1_fields = [getattr(obj, 'id') for obj in list1]
        list2_fields = [obj.get('id') for obj in list2]
        return list(set(list1_fields) & set(list2_fields))    

    def create(self, validated_data):
        logger.info("Validated Data %s" % validated_data)   
        articles_data = validated_data.pop('articles', [])
        logger.info("Article_data %s" % articles_data)   

        order = Order.objects.create(**validated_data)

        total_price = 0            
        total_tax = 0 
        for article_data in articles_data:                
            try:
                article = Article.objects.get(reference=article_data.get('reference'))    
                logger.info("Article with reference %s exists." % article_data)   
                order.articles.create(article=article, amount=article_data.get('amount'))                           
                total_price += article.price * article_data.get('amount')    
                total_tax +=  article.price * (1 + article.tax/100) * article_data.get('amount')         
            except Article.DoesNotExist:   
                logger.info("Article with reference %s does not exists." % article_data.get('reference'))                                         
        order.price = total_price
        order.tax_price = total_tax
        order.create_date = self.context['request'].data.get('create_date')
        order.save()
        return order
    
    def update(self, instance, validated_data):
        articles_data = validated_data.pop('articles', [])

        common_articles = self._common_articles(instance.articles.all(), articles_data)
        for order_article in instance.articles.all():
            if order_article.id in common_articles:
                order_article.amount = next(article['amount'] for article in articles_data if article.get('id') == order_article.id)
                order_article.save()
            else:
                order_article.delete()

        for article_data in articles_data: 
            try:
                id=article_data.get('id')
                if id is None:
                    article = Article.objects.get(reference=article_data.get('reference'))      
                    instance.articles.create(article=article, amount=article_data.get('amount'))                                                   
            except Article.DoesNotExist:   
                logger.info("Article with reference %s does not exists." % article_data.get('reference')) 

        total_price = 0    
        total_tax = 0
        for article in instance.articles.all():
            total_price += article.article.price * article.amount
            total_tax += article.article.price * (1 + article.article.tax/100) * article.amount
        instance.price = total_price
        instance.tax_price = total_tax
        instance.creation_date = validated_data.get('creation_date', instance.creation_date)
        instance.save()
        return instance
    
    
