import uuid
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

User = get_user_model()



class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    # pre_social_login ഫങ്ഷൻ ഇതിന് താഴെ നിങ്ങളുടെ പഴയതുപോലെ തന്നെ തുടരട്ടെ...
    
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        
        # യൂസർക്ക് ഇതിനകം ഒരു ഐഡി ഉണ്ടെങ്കിൽ (പഴയ യൂസർ ആണെങ്കിൽ) ഒന്നും ചെയ്യേണ്ടതില്ല
        if user.id:
            return

        if not user.username and user.email:
            # ഇമെയിലിന്റെ ആദ്യ ഭാഗം എടുക്കുന്നു (e.g., niiihalyp)
            base_username = user.email.split('@')[0]
            username = base_username
            
            # ഈ യൂസർനെയിം ഓൾറെഡി ഡാറ്റാബേസിൽ ഉണ്ടോ എന്ന് നോക്കുന്നു
            # ഉണ്ടെങ്കിൽ അതിന്റെ കൂടെ റാൻഡം നമ്പറുകൾ ചേർത്ത് യുണീക് ആക്കുന്നു
            while User.objects.filter(username=username).exists():
                # ഉദാഹരണത്തിന്: niiihalyp_4a1b
                username = f"{base_username}_{uuid.uuid4().hex[:4]}"
            
            # ഒടുവിൽ യുണീക് ആയ യൂസർനെയിം സെറ്റ് ചെയ്യുന്നു
            user.username = username
