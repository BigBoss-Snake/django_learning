from rest_framework import serializers
from book.models import Books, Category, Value
from users.models import User


class CategorySerialazer(serializers.Serializer):
    category = serializers.CharField(max_length=200)

    class Meta:
        model = Category
        fields = ['category']


class SearchSerialazer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    category = CategorySerialazer(many=True)


class ValueSerialazer(serializers.Serializer):
    title = serializers.CharField(max_length=15)


class BookSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=200, label='lol')
    title = serializers.CharField(max_length=200)
    author_book = serializers.CharField(max_length=200)
    category = CategorySerialazer(many=True)
    price = serializers.SerializerMethodField('get_calculate_price')
    value = ValueSerialazer(many=False)

    class Meta:
        model = Books
        fields = ('author', 'title', 'author_book')

    def create(self, validated_data):
        return Books.objects.create_book(**validated_data)

    def validate(self, data):
        author = data.get('author', None)
        title = data.get('title', None)
        author_book = data.get('author_book', None)
        category_book = data.get('category', None)
        value_book = data.get('value', None)
        price_book = data.get('price', None)

        if author is None:
            raise serializers.ValidationError(
                'The name author is not enered'
            )

        if title is None:
            raise serializers.ValidationError(
                'The name of the book is not entered'
            )

        if author_book is None and User.objects.get(email=author_book).count():
            raise serializers.ValidationError(
                'The author of the book is not entered'
            )

        if category_book is None:
            raise serializers.ValidationError(
                'The category book of the book is not entered'
            )

        if not User.objects.filter(email=author):
            raise serializers.ValidationError(
                'This author does not exist'
            )
        return {
                'author': author,
                'title': title,
                'category': category_book,
                'author_book': author_book,
                'value': value_book,
                'price': price_book
            }

    def get_calculate_price(self, obj):
        eur_curs = Value.objects.get(title='Eur').count
        usd_curs = Value.objects.get(title='Usd').count

        if obj.value == 'Eur':
            obj.value = 'Rub'
            return obj.price * eur_curs
        elif obj.value == 'Usd':
            obj.value.title = 'Rub'
            return obj.price * usd_curs
        return obj.price
