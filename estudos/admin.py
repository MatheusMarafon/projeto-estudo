# estudos/admin.py
from django.contrib import admin
from .models import Question, Option  # Importe os novos modelos


# Para exibir as opções dentro da página da pergunta
class OptionInline(admin.TabularInline):
    model = Option
    extra = 3  # Mostra 3 campos de opção por padrão


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


# Registre os modelos
admin.site.register(Question, QuestionAdmin)
# Não precisamos registrar Option separadamente, pois já está "inline"
