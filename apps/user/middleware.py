from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings

NO_LOGIN_LINKS = ['/user/login/','/s/','/admin/','/rss/','/register/']

class LoginMiddleware():
    def process_request(self,request):
        
        public_link = False
        
        path = request.path
        
        if path.startswith('/django.fcgi'):
            path = path[12:]
        
        # @TODO: Zmienic sposob okreslania publicznych linkow
        for link in NO_LOGIN_LINKS:
            if path.startswith(link):
                public_link = True
        
        if not request.user.is_authenticated():
            if not public_link:
                # @TODO: w next dodac parametry query
                return HttpResponseRedirect(settings.LOGIN_URL+'?next='+path)
                
from django.template import loader
class ErrorMiddleware():
    def process_exception(self, request, exception):
        enc_message = "%s" % (exception)
        return HttpResponse(loader.render_to_string('system/error500.html',{
            'message' : str(enc_message).encode('base64').encode('rot13')
        }), status=500 )


USER_MESSAGES_KEY = '__user_messages__'

class UserMiddleware():
    def process_request(self,request):

        def user_message(text,className='info'):
            request.session.setdefault(USER_MESSAGES_KEY,[]).append({ 'className' : className, 'text' : text })

        def get_user_messages():
            messages = request.session.get(USER_MESSAGES_KEY,[])
            if messages:
                del request.session[USER_MESSAGES_KEY]
            return messages

        # nakladka - maly alians
        request.user_success = lambda text: request.user_message(text,'success')
        request.user_error = lambda text: request.user_message(text,'error')

        request.user_message = user_message
        request.get_user_messages = get_user_messages
        
def user_messages(request):
    return { 'user_messages' : ['a','b','v'] }

