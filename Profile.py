from getpass import getuser
from os import popen, system
from sys import platform
from re import search
import logging


class Profile(object):
    """docstring for Profile"""
    def __init__(self, userType):
        super(Profile, self).__init__()
        self.PATH_FILE = self.__getPathFile()
        self.LOAD_PROFILE = False
        self.userProfile = None
        self.NAME_FILE = 'prefs.js'
        self.document = ''
        self.USER_TYPE = userType
        self.local_logger = logging.getLogger('super_logger')

    def getProfile(self):
        self.document = popen('cat ' + self.PATH_FILE +self.NAME_FILE).read()

    def setParameters(self, key, value):
        if type(value) == str:
            value = '"'+value+'"'
        elif isinstance(value,bool):
            if value:
                value='true'
            else:
                value='false'
                
        parameterReplace = search(r'user_pref\("'+key+'".*', self.document)
        if parameterReplace:
            self.document = self.document.replace(parameterReplace.group(0), 'user_pref("{}", {});'.format(key, value))
        else:
            self.document += 'user_pref("{}", {});\n'.format(key, value)


    def deleteParameter(self, key):

        parameterReplace = search(r'user_pref\("'+key+'".*', self.document)
        if parameterReplace:
            self.document = self.document.replace(parameterReplace.group(0), '')

    def saveProfile(self, userAgent=None, userType=None):
        connection = self.__mongoconexion()
        db_name = self.__set_database(connection)
        if self.LOAD_PROFILE:
            db_name[self.MONGODB_COLLECTION].update({'_id':self.userProfile['_id']},{'$set':{'cookies':self.__getCookies()}})
        else:
            dictInsert = {'userAgent':userAgent, 'cookies':self.__getCookies(), 'userType':userType}
            db_name[self.MONGODB_COLLECTION].insert(dictInsert)

        connection.close()

    def loadProfile(self, userType=None):
        self.LOAD_PROFILE = True
        connection = self.__mongoconexion()
        db_name = self.__set_database(connection)
        self.userProfile = db_name[self.MONGODB_COLLECTION].aggregate([{'$sample':{'size':1}}])
        # self.userProfile = db_name[self.MONGODB_COLLECTION].aggregate([
        #                                                               {'$match':{
        #                                                                           'userType':userType
        #                                                                         }
        #                                                               },
        #                                                               {
        #                                                               '$sample':{
        #                                                                           'size':1
        #                                                                         }
        #                                                               }
        #                                                             ])
        self.userProfile = list(self.userProfile)[0]
        cookies = popen('cd '+self.PATH_FILE+'; pwd').read()
        cookies = cookies.replace('\n','')  
        system("cd "+self.PATH_FILE+"; rm cookies.sqlite; touch cookies.sqlite;")
        cookiesFileWrite = open(cookies+'/cookies.sqlite','wb')     
        cookiesFileWrite.write(self.userProfile['cookies'])

        return self.userProfile['userAgent']
        

    def saveFile(self, close=False, userAgent=None, userType=None):
        # system("cd "+self.PATH_FILE+"; rm cookies.sqlite; touch cookies.sqlite; rm "+self.NAME_FILE+";echo '" +self.document+"' > "+self.NAME_FILE)
        if close:
            system("cd "+self.PATH_FILE+"; rm "+self.NAME_FILE+";echo '" +self.document+"' > "+self.NAME_FILE)
            self.saveProfile(userAgent=userAgent, userType=userType)
        elif "Recurrent" in self.USER_TYPE:
            self.loadProfile()
            system("cd "+self.PATH_FILE+"; rm "+self.NAME_FILE+";echo '" +self.document+"' > "+self.NAME_FILE)
        else:
            system("cd "+self.PATH_FILE+"; rm cookies.sqlite; touch cookies.sqlite; rm "+self.NAME_FILE+";echo '" +self.document+"' > "+self.NAME_FILE)

    def __getCookies(self):
        cookies = popen('cd '+self.PATH_FILE+'; pwd').read()
        cookies = cookies.replace('\n','')          
        cookiesFile = open(cookies+'/cookies.sqlite','rb')
        return cookiesFile.read()


    def __getPathFile(self):

        # Regresa el sistema operativo en el que se está ejecutando
        if platform == "linux" or platform == "linux2":
        # linux
            return '/home/'+str(getuser())+'/.mozilla/firefox/*.default*/'
        elif platform == "darwin":
        # OS X
            return '/Users/'+str(getuser())+'/Library/Application\ Support/Firefox/Profiles/*.default*/'
        # elif platform == "win32":



if __name__ == '__main__':
    uw = Profile("new")
    uw.getProfile()
    #uw.setParameters("browser.cache.disk.smart_size.first_run",True)
    uw.setParameters("browser.sessionstore.resume_from_crash",False)
    uw.saveFile()
    # uw.set_parameters(':v_2','Hola_2')