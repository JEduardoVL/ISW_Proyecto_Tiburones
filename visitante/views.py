from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

class VisitanteHomeView(TemplateView):
    template_name = 'visitante/home.html'

class VisitanteBuscarView(TemplateView): 
    template_name = 'visitante/buscar.html'

class VisitanteCbuscarView(TemplateView): 
    template_name = 'visitante/como_buscar.html'

class VisitantePfrecuentesView(TemplateView): 
    template_name = 'visitante/preguntas_frecuentes.html'

class VisitanteContactoView(TemplateView): 
    template_name = 'visitante/contactanos.html'

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        template = render_to_string('contacto.html', {
            'name': name,
            'email': email,
            'message': message
        })

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['aeneta.re@gmail.com']
        )

        email.fail_silently = False
        email.send()

        messages.success(request,' Correo enviado con exito.')
        return redirect('visitante:contactanos')
    
    # si no es la solicitus esperada
    return render(request, 'visitante:home.html')