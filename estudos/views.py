# Imports organizados e sem duplicatas
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import random
import json
import google.generativeai as genai
from google.generativeai.types import (
    GenerationConfig,
)  # Import para controlar o chatbot

# 1. IMPORT DO MODELO QUE ESTAVA FALTANDO
from .models import Question


def home(request):
    """Página inicial do sistema de estudos"""
    return render(request, "estudos/home.html")


def django_view(request):
    """Página de estudos sobre Django"""
    return render(request, "estudos/django_content.html")


def bootstrap_view(request):
    """Página de estudos sobre Bootstrap 4"""
    return render(request, "estudos/bootstrap_content.html")


def rd_station_view(request):
    """Página de estudos sobre API RD Station"""
    return render(request, "estudos/rd_station_content.html")


def d4sign_view(request):
    """Página de estudos sobre API D4Sign"""
    return render(request, "estudos/d4sign_content.html")


def atividades_view(request):
    """Página de Atividades Interativas com Bootstrap"""
    return render(request, "estudos/atividades.html")


def quiz_questions_api(request):
    """
    API que lê o arquivo questions.json, adapta o formato e retorna 4 perguntas aleatórias.
    """
    file_path = settings.BASE_DIR / "estudos" / "questions.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. ACESSA A LISTA DENTRO DA CHAVE "perguntas"
        all_questions = data["perguntas"]

        random.shuffle(all_questions)
        selected_questions = all_questions[:4]

        # 2. TRANSFORMA OS DADOS PARA O FORMATO QUE O FRONTEND ESPERA
        formatted_questions = []
        for i, q in enumerate(selected_questions):
            options_list = []
            correct_id = None

            # Cria as opções no formato { "id": ..., "text": "..." }
            for j, opt_text in enumerate(q["opcoes"]):
                option_id = (i * 100) + j  # Cria um ID único para a opção
                options_list.append({"id": option_id, "text": opt_text})

                # Se esta for a resposta correta, guarda o ID
                if opt_text == q["resposta_correta"]:
                    correct_id = option_id

            formatted_questions.append(
                {
                    "id": q["id"],
                    "text": q["pergunta"],
                    "options": options_list,
                    "correct_answer_id": correct_id,
                }
            )

        return JsonResponse(formatted_questions, safe=False)

    except FileNotFoundError:
        return JsonResponse(
            {"error": "Arquivo de perguntas não encontrado."}, status=500
        )
    except Exception as e:
        return JsonResponse({"error": f"Erro no servidor: {str(e)}"}, status=500)


@csrf_exempt
def chatbot_send(request):
    """Processa mensagens do chatbot"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not settings.GEMINI_API_KEY:
                return JsonResponse(
                    {
                        "response": "A chave de API do Gemini não está configurada no servidor.",
                        "status": "error",
                    }
                )

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("models/gemini-flash-latest")

            context = """Você é um assistente especializado em desenvolvimento web, focado em Django, Bootstrap 4, e APIs.
            REGRAS IMPORTANTES:
            1. Seja sempre conciso e direto ao ponto. Suas respostas devem ser curtas.
            2. Responda como se estivesse em uma conversa de chat, não escrevendo um artigo.
            3. Use no máximo 3 ou 4 frases, a menos que o usuário peça explicitamente para elaborar.
            4. Use blocos de código apenas para exemplos essenciais e curtos."""

            # ===== LIMITE DE TOKENS AUMENTADO =====
            generation_config = GenerationConfig(
                max_output_tokens=800,  # Aumentado de 200 para 800 para dar mais "espaço" para a IA.
                temperature=0.7,
            )

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]

            response = model.generate_content(
                f"{context}\n\nUsuário: {user_message}",
                generation_config=generation_config,
                safety_settings=safety_settings,
            )

            # Checagem final: se a resposta estiver vazia por algum outro motivo, retorna um erro amigável.
            if not response.parts:
                # Usa o prompt_feedback para tentar dar mais detalhes, se houver.
                feedback = (
                    response.prompt_feedback
                    if hasattr(response, "prompt_feedback")
                    else "Nenhum detalhe adicional."
                )
                return JsonResponse(
                    {
                        "response": f"A resposta foi bloqueada por um motivo desconhecido. Feedback: {feedback}",
                        "status": "error",
                    }
                )

            return JsonResponse({"response": response.text, "status": "success"})

        except Exception as e:
            return JsonResponse(
                {
                    "response": f"Ocorreu um erro no servidor: {str(e)}",
                    "status": "error",
                },
                status=500,
            )

    return JsonResponse({"error": "Método não permitido"}, status=405)
