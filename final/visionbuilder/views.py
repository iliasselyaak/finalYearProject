
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Page


class PageListCreate(APIView):
    def get(self, request):
        if request.user.is_authenticated: # Check if the user is authenticated.
            pages = Page.objects.filter(user=request.user)
            pages_data = []

            for page in pages: # Loop through the pages and append the data to the pages_data list.
                pages_data.append({
                    'id': page.id,
                    'user': page.user.username,
                    'name': page.name,
                    'content': page.content,
                    'public': page.public,
                    'html': page.html,
                    'css': page.css
                })

            return Response(pages_data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED) # Return 401 Unauthorized if the user is not authenticated.

    def post(self, request):
        if request.user.is_authenticated:
            name = request.data.get('name')
            content = request.data.get('content')

            page = Page.objects.create(user=request.user, name=name, content=content) # Create a new page.
            page_data = {
                'id': page.id,
                'user': page.user.username,
                'name': page.name,
                'content': page.content,
                'public': page.public,
                'html': page.html,
                'css': page.css
            }

            return Response(page_data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class PageRetrieveUpdate(APIView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            page = Page.objects.get(pk=pk, user=request.user)
            page_data = { # Create a dictionary with the page data.
                'id': page.id,
                'user': page.user.username,
                'name': page.name,
                'content': page.content,
                'public': page.public,
                'html': page.html,
                'css': page.css
            }

            return Response(page_data) # Return the page data.
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        if request.user.is_authenticated:
            page = Page.objects.get(pk=pk, user=request.user)
            data = request.data
            # Update the page data.
            page.name = data.get('name', page.name)
            page.content = data.get('content', page.content)
            page.public = data.get('public', page.public)
            page.html = data.get('html', page.html)
            page.css = data.get('css', page.css)

            page.save() # Save the page.
            # Create a dictionary with the new page data.
            page_data = {
                'id': page.id,
                'user': page.user.username,
                'name': page.name,
                'content': page.content,
                'public': page.public,
                'html': page.html,
                'css': page.css
            }

            return Response(page_data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, pk): 
        if request.user.is_authenticated:
            page = Page.objects.get(pk=pk, user=request.user)
            page.delete() # Delete the page.
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class PublicPages(APIView):
    authentication_classes = [] # Disable authentication
    permission_classes = [] # Disable permissions
    def get(self, request):
        public_pages = Page.objects.filter(public=True) # Get all public pages.
        public_pages_data = []

        for page in public_pages:
            public_pages_data.append({
                'id': page.id,
                'user': page.user.username,
                'name': page.name,
            })

        return Response(public_pages_data)
    
class PublicPagesCode(APIView):
    authentication_classes = [] # Disable authentication
    permission_classes = [] # Disable permissions
    def get(self, request, pk):
        public_pages = Page.objects.filter(pk=pk) # Get all public pages with id.
        public_pages_data = []

        for page in public_pages:
            public_pages_data.append({
                'html': page.html,
                'css': page.css
            })

        return Response(public_pages_data)

