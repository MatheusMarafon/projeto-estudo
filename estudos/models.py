from django.db import models


class Question(models.Model):
    text = models.CharField("Texto da Pergunta", max_length=500)

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE
    )
    text = models.CharField("Texto da Opção", max_length=200)
    is_correct = models.BooleanField("É a correta?", default=False)

    def __str__(self):
        return f"{self.text} (para: {self.question.text[:30]}...)"
