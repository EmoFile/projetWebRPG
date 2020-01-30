"""projetwebrpg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

from app.views import IndexView, GenerateCharacterView, CharacterDetailView, \
    SignUpView, LogInView, PlayGameView, \
    DropItem, EnemyList, ChangeItem, UseItem, PlayRound, NextEnemyView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('generateCharacterByPk/<int:pk>', GenerateCharacterView.as_view(),
         name='generateCharacterByPk'),
    path('characterDetail/<int:pk>', CharacterDetailView.as_view(),
         name='characterDetail'),
    path('playGame/<int:pk>', PlayGameView.as_view(), name='playGame'),
    path('signUp/', SignUpView.as_view(), name='signUp'),
    path('logIn/', LogInView.as_view(), name='logIn'),
    path('logOut/', LogoutView.as_view(), name='logOut'),
    path('dropItem', DropItem, name='dropItem'),
    path('quantity/<int:partyPk>/<int:consumablePk>', UseItem,
         name='useItem'),
    path('changeItem/<int:partyPk>/<str:stuffClassName>/<int:stuffPk>',
         ChangeItem, name='changeItem'),
    path('ArticleListView/', EnemyList.as_view(), name='listEnemy'),
    path('playRound/<int:pkParty>/<int:pkEnemy>', PlayRound.as_view(), name='playRound'),
    path('nextEnemy/<int:pkParty>/<int:pkEnemy>', NextEnemyView.as_view(), name='nextEnemy')

]
