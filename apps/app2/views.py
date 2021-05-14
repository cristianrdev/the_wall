from django.shortcuts import render, redirect
from apps.app1.models import User
from .models import Message, Comment
from django.contrib import messages

# Create your views here.
def show_wall(request):
    #si no existe la sesión redirige al home
    if 'id' and 'firstname' and 'lastname' not in  request.session :
        return redirect('/')
    else:
        #si existe sesión graba un diccionario con todos los mensajes comentarios y usuarios
        all_users = User.objects.all()
        all_messages = Message.objects.all()
        all_comments = Comment.objects.all()
        context = {
            'users' : all_users,
            'messages' : all_messages,
            'comments' : all_comments,
            'id_actual_user' : request.session['id'],
        }
        # print(all_users.first_name)
        return  render(request,'wall.html', context)


def postmessage(request):
    errors = Message.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
        return redirect('/wall')
    # si NO hay errores en el ingreso del formulario
    else: 
        print('es un post')
        this_user = User.objects.get(id= int(request.session['id']))
        new_message = Message.objects.create(message = request.POST['messagesHTML'], users = this_user)
        return redirect('/wall')

def makecomment(request):
    errors = Comment.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
        return redirect('/wall')
    # si NO hay errores en el ingreso del formulario
    else: 
        comment_content = request.POST['commentHTML']
        id_user_of_the_message = request.POST['user_id_of_the_message']
        message_id = request.POST['message_id_to_comment']
        

        this_user = User.objects.get(id= int(id_user_of_the_message))
        this_message = Message.objects.get(id = int(message_id))
        new_comment = Comment.objects.create(
            comment = comment_content, 
            users = this_user,
            messages = this_message,
            )
        return redirect('/wall')


def delete_message(request):
    print('borrando mensaje con id')
    print(request.POST['id_of_message'])
    id_message = request.POST['id_of_message']
    message_to_delete = Message.objects.get(id=int(id_message))
    print(message_to_delete.message)
    message_to_delete.delete()
    return redirect('/wall')


def delete_comment(request):
    print('borrando el comentario con id')
    print(request.POST['id_commentHTML'])
    id_comment = request.POST['id_commentHTML']
    comment_to_delete = Comment.objects.get(id=int(id_comment))
    print(comment_to_delete.comment)
    comment_to_delete.delete()
    return redirect('/wall')