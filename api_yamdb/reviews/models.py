from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.text

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.text
    
class Rating(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    grade = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Рейтинги'
        verbose_name = 'Рейтинг'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title"], name="unique_user_title"
            ),
        ]
