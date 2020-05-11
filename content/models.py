from django.db import models

# Create your models here.


class CategoryTable(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'cms_category_table'


class CurriculumTable(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(CategoryTable, models.CASCADE, db_column='category')

    class Meta:
        managed = False
        db_table = 'cms_curriculum_table'


class EssayTable(models.Model):
    name = models.CharField(max_length=60)
    curriculum = models.ForeignKey(CurriculumTable, models.CASCADE, db_column='curriculum')
    submit_time = models.DateTimeField()
    content = models.TextField(null=True)
    amount_of_reading = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'cms_essay_table'
        ordering = ['id']
