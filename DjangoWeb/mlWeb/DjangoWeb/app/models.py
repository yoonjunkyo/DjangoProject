"""
Definition of models.
"""

from django.db import models

# Create your models here.
class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    
        # 게시글의 제목(postname)이 Post object 대신하기
    def __str__(self):
        return self.postname