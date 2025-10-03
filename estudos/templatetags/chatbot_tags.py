from django import template

register = template.Library()


@register.inclusion_tag("estudos/partials/chatbot_widget.html")
def chatbot_widget():
    # Esta tag não precisa de lógica, apenas de renderizar o template.
    # O dicionário retornado (mesmo vazio) é passado como contexto para o template.
    return {}
