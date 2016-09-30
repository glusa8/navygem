'''navygem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
'''
from navygem.settings import ENV
from navygem.settings import STATIC_ROOT
from navygem.settings import STATIC_URL
from navygem.schema import schema
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from django.views.decorators.csrf import ensure_csrf_cookie

from django_graphiql.views import GraphiQL
from graphene.contrib.django.views import GraphQLView


urlpatterns = [
    url(r'^api/graphql$', GraphQLView.as_view(schema=schema)),
] + static(STATIC_URL, document_root=STATIC_ROOT)

if ENV != 'PROD':
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
        url(r'^graphiql$', ensure_csrf_cookie(GraphiQL.as_view())),
    ]
