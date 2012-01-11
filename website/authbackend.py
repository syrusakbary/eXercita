try:
    import ldap as _ldap
except:
    class UCMLogin (object):
        def __init__(self,dn,password): pass
        def login (self,mail,password=False,out=['cn']):
            raise Exception('LDAP module not installed')
else:
    class UCMLogin (object):
        server = 'ldap://ldap.sim.ucm.es'
        bindsearch = 'dc=ucm,dc=es'

        def __init__(self,dn,password):
            self.ldap = _ldap.initialize(self.server)
            self.dn = dn
            try:
                self.ldap.simple_bind_s(dn.encode('utf-8'),password.encode('utf-8'))
            except _ldap.INVALID_CREDENTIALS:
                raise Exception('Credenciales incorrectas')

        def search (self,base=None,filter='(objectClass=*)',out=None):
            base = base or self.bindsearch
            return list(self.ldap.search_s(base,_ldap.SCOPE_SUBTREE,filter,out))

        def data (self):
            return self.ldap.search_s(self.dn,_ldap.SCOPE_BASE)[0][1]

        def mod_add (self,key,value):
            return [( _ldap.MOD_ADD, key, value )]

        def mod_replace (self,key,value):
            return [( _ldap.MOD_REPLACE, key, value )]

        def mod_delete (self,key,value):
            return [ (_ldap.MOD_DELETE, key,value) ]

        def modify (self, mod_attrs):
            return self.ldap.modify_s(self.dn, mod_attrs)

        def user_data (self,mail,out=None):
            filter_ds = '(|(|(mail=%s)(mailAlternateAddress=%s))(mailAlternateAddress=*:%s))'%(mail,mail,mail);
            entries = self.search(None,filter_ds,out)
            if len(entries)>1: raise Exception('Se ha encontrado mas de un username con ese mail')
            if len(entries)==0: raise Exception('No se ha encontrado el email en el directorio activo')
            return entries[0]

        def login (self,mail,password=False,out=['cn']):
            dn,entry = self.user_data(mail)
            return UCMLogin(dn,password), entry
        
        def __str__ (self):
            return str(self.dn)

# admin_dn = 'uid=admWebUcm,o=userAdmin,dc=ucm,dc=es'
# admin_pass = '.lo9,ki8zaq1'

# a = UCMLogin(admin_dn,admin_pass)
# b= a.login('sannieto@estumail.ucm.es','28bc600b')
# print a.data()



from django.conf import settings
from django.contrib.auth.models import User, check_password

class UCMBackend(object):

    supports_inactive_user = False
    ucmlogin = UCMLogin(settings.LDAP_ADMIN_DM,settings.LDAP_ADMIN_PASS)
    def authenticate(self, username=None, password=None):
        try:
            login,data = self.ucmlogin.login(username,password)
        except:
            pass
        else:
            try:
                un = data.get('irisPersonalUniqueID',[username])[0]
                user = User.objects.get(username=un)
            except User.DoesNotExist:
                user = User(username=un)
                user.email = username
                user.set_password(password)
                user.first_name = data.get('givenName',[''])[0].title()
                user.last_name = data.get('sn',[''])[0].title()
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# print b.modify(b.mod_add('mailAlternateAddress','syrus'))
#print a.search('cn=Top-level Admin Role,dc=ucm,dc=es')

#print b, b.data()
#print a.user_data('cgr@sip.ucm.es')

# a.login('sannieto@estumail.ucm.es','28bac600b')
