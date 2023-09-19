from haystack import indexes
from .models import BlogPost

class BlogPostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    content = indexes.EdgeNgramField(model_attr='content')
    
    def get_model(self):
        return BlogPost
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()