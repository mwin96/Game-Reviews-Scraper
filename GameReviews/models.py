from django.db import models
import django_tables2 as tables

# Create your models here.
# models.py

class Reviews(models.Model):
    website = models.CharField(max_length=200, default="")

    link = models.CharField(max_length=2083, default="")
    #Maybe try URL field? for Link 
    title = models.CharField(max_length=200, default = "")

    developer = models.CharField(max_length=200, default = "")

    releaseDate = models.DateField(max_length=200)

    score = models.FloatField(max_length=200)
    
    steamReview = models.CharField(max_length=200, default = "")

    consoles = models.CharField(max_length=200)


# class Feature(BaseTable):
#     ...
#     actions = tables.TemplateColumn("""
#     {% if not record.featured_item %}
#     {% url 'add_feature' pk=record.pk as url_ %}
#     {% label_link url_ 'Add to Features' %}
#     {% else %}
#     {% url 'remove_feature' pk=record.pk as url_ %}
#     {% label_link url_ 'Remove From Features' %}
#     {% endif %}
#     """, attrs=dict(cell={'class': 'span1'}))

class ReviewsTable(tables.Table):
    # name = tables.TemplateColumn('<a href="{{record.link}}">{{record.title}}</a>', order_by= "title", attrs={"td" : {"bgcolor": "red"}} )
    name = tables.TemplateColumn('<a href="{{record.link}}">{{record.title}}</a>', order_by= "title")
    score = tables.TemplateColumn(
    """
    {% if record.website == 'Steam' %}
        {% if record.steamReview == "Very Positive" or record.steamReview == "Overwhelmingly Positive" %}
            <div class="score great"> 
        {% elif record.steamReview == "Mostly Positive" or record.steamReview == "Positive" %}
            <div class ="score good">
        {% else %}
            <div class = "score bad">
        {% endif %}
        {{ record.steamReview }}
    {% else %}
        {% if record.score > 8 %}
            <div class = "great">
        {% elif record.score >= 7 %} 
            <div class = "good">
        {% else %}
            <div class = "bad">
        {% endif %}
        {{record.score}}
    {% endif %}
    </div>
    """)
    releaseDate = tables.Column(verbose_name= 'Released Date')
    # score = tables.Column(attrs={"td" : {"class": "great"}})
    class Meta:
        model = Reviews
        attrs = {'class': 'baka'}
        exclude = ('id', 'steamReview', )
        fields = ('name', 'releaseDate', 'score', 'consoles', 'developer',  )
        # exclude_columns = ("website", )