from django.db import models

class Child(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    pictures = models.JSONField(default=list)
    description = models.CharField(max_length=150)
    adder = models.ForeignKey("account.Role", on_delete=models.CASCADE)
    comment = models.CharField(max_length=150)
    STATUS_CHOICES = [
        ('r', 'Reported'),
        ('c', 'Checked'),
        ('f','Follow-Up'),
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='r',
    )
    def __str__(self):
        return self.name
