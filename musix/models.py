from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Audio(models.Model):
    KEY_CHOICES = (
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'),
        ('Ab', 'Ab'), ('Bb', 'Bb'), ('Db', 'Db'), ('Eb', 'Eb'), ('Gb', 'Gb'),
        ('Am', 'Am'), ('Bm', 'Bm'), ('Cm', 'Cm'), ('Dm', 'Dm'), ('Em', 'Em'), ('Fm', 'Fm'), ('Gm', 'Gm'),
        ('Abm', 'Abm'), ('Bbm', 'Bbm'), ('Dbm', 'Dbm'), ('Ebm', 'Ebm'), ('Gbm', 'Gbm'),
    )
    INSTRUMENTS = (
        ('Vocals', 'Vocals'), ('Guitar', 'Guitar'), ('Bass', 'Bass'), ('Keyboard', 'Keyboard'), ('Drums', 'Drums'), ('Violin', 'Violin')
    )

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=100)
    instrument = models.CharField(max_length=100, choices=INSTRUMENTS, default="Guitar")
    key = models.CharField(max_length=100, choices=KEY_CHOICES, default="A")
    mp3 = models.FileField(upload_to='audio/mp3s/')
    sample_count = models.IntegerField(max_length=100, default=0)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.mp3.delete()
        super().delete(*args, **kwargs)


class Sample(models.Model):
    main = models.ForeignKey(Audio, related_name="main", on_delete=models.CASCADE)
    sub = models.ForeignKey(Audio, related_name="sub", on_delete=models.CASCADE)


# make unique titles
