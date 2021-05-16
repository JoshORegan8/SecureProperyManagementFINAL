from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


# Sets which roles have permissions to view a page
def authorized_users(authorized_roles=[]):
    def dec(view_func):
        # Wrapper function, assigning an initial value to userGroup
        def wFunc(request, *args, **kwargs):
            userGroup = None
            # checks that the users group indeed is inside the DB and sets the name
            if request.user.groups.exists():
                userGroup = request.user.groups.all()[0].name
            # If the group the user is in is authorized, the page will display
            if userGroup in authorized_roles:
                return view_func(request, *args, **kwargs)
            # if the group is not authorized to view the page they are redirected
            else:
                # Refer user back to the page/view they came from
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return view_func(request, *args, **kwargs)
        return wFunc
    return dec


# Restricts access for users that are not logged in
def notLoggedIn(view_func):
    def wFunc(request, *args, **kwargs):
        # Checks if the user accessing the view function is logged in or not
        if request.user.is_authenticated:
            # if authenticated, the view will display
            return view_func(request, *args, **kwargs)
        else:
            # if not authenticated, they will be directed to the login page
            return redirect('/login')
    return wFunc
