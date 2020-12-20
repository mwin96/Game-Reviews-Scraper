import django_tables2 as tables
from .models import Reviews

class ReviewsTable(tables.Table):
    # name = tables.TemplateColumn('<a href="{{record.link}}">{{record.title}}</a>', order_by= "title", attrs={"td" : {"bgcolor": "red"}} )
    name = tables.TemplateColumn('<a href="{{record.link}}">{{record.title}}</a>', order_by= "title", verbose_name= "Game Title")
    score = tables.TemplateColumn(
    """
    {% if record.website == 'Steam' %}
        {% if record.steamReview == "Very Positive" or record.steamReview == "Overwhelmingly Positive" %}
            <div class="score great"> 
        {% elif record.steamReview == "Mostly Positive" or record.steamReview == "Positive" %}
            <div class ="score good">
        {% elif record.steamReview == "N/A" %}
            <div class ="notAvailable">
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
        # attrs = {'class': 'test'}
        exclude = ('id', 'steamReview', )
        fields = ('name', 'releaseDate', 'score', 'consoles', 'website', 'developer',  )
        order_by = '-score'
        attrs = {"class": "paleblue"}
        per_page = 30
        # exclude_columns = ("website", )