import requests

class api_requests():
    def __init__(self,baseUrl,user_name,pwd):
        self.base_url = baseUrl
        self.api_session = requests.Session()
        #authenticate
        response = self.api_session.post('%s/d2l/lp/auth/login/login.d2l'%self.base_url,headers= {'content-type': 'application/x-www-form-urlencoded'},
        data = {'userName':user_name, 'password':pwd})
        response = self.api_session.get('%s/d2l/lp/auth/login/ProcessLoginActions.d2l'%self.base_url)

    def issueGetRequest(self,requestString,query={}):
        url = '%s/%s'%(self.base_url,requestString)

        if query:
            response = self.api_session.get(url,json=query)
        else:
            response = self.api_session.get(url)
        return response
