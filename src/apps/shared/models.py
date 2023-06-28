from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class DocumentsUniversity(BaseModel):
    class Meta:
        verbose_name = "Документ университета"
        verbose_name_plural = "Документы университета"

    title = models.CharField(max_length=150, blank=False)
    document_name = models.CharField(max_length=100, blank=False)  # хранит строку, которая представляет имя файла
    # эквивалентно varchar(100) NOT NULL  - 100 символов ограничение
    path = models.FileField(upload_to='documents_university/', null=True)
    date_added = models.DateField(blank=False)
