#############################
#        Created by         #
#     Harrison Crossley     #
#                           #
#      Version - 1.0        #
#                           #
#############################
from lib2to3.pgen2 import token
import urllib.request
import urllib.parse
import json
import pandas as pd
import inquirer

print("Unisolation Tool:")
print("\n")

#Obtain machines form CSV
df = pd.read_csv("Machine_list.csv")
machine_df = pd.DataFrame(df['Machine'])

#Add user comment
Isolation_comment = input("Please add a comment:")

#Get AAD token
def get_token():
    tenantId = "<Add tenantid>"            
    appId = "<Add appId>"               
    appSecret = "<Add app secret value>"

    url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenantId)
    resourceAppIdUri = 'https://api-uk.securitycenter.microsoft.com'
    body = {
    'resource' : resourceAppIdUri,
    'client_id' : appId,
    'client_secret' : appSecret,
    'grant_type' : 'client_credentials'
}

    data = urllib.parse.urlencode(body).encode("utf-8")

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    jsonResponse = json.loads(response.read())
    aadToken = jsonResponse["access_token"]
    return aadToken

#Isolate machine(s)
def mdatp_Unisolate_machine(auth_token, comment):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + auth_token
    }

    body = {
        'Comment' : comment,
    }
    for (index, row) in machine_df.iterrows():
        url = "https://api-uk.securitycenter.windows.com/api/machines/"+row['Machine']+"/unisolate"
        data = str(json.dumps(body)).encode("utf-8")
        req = urllib.request.Request(url=url,data=data,headers=headers)
        response = urllib.request.urlopen(req)
        jsonResponse = json.loads(response.read())
        if(jsonResponse['status'] == "Pending"):
            print("Release of Machine {} from isolation initiated".format(row['Machine']))
        else:
            print("Release of Machine {} from isolation failed".format(row['Machine']))
        
# Final user check
Double_check_question = [
    inquirer.List('Double_check',message="You are going to release "+ str(len(machine_df['Machine']))+" machine(s) from isolation. Are you sure ?", choices=["Yes","No"], default="No")
]
Double_check_answer = inquirer.prompt(Double_check_question)

def Double_Check():
    if(Double_check_answer['Double_check']=="No"):
        print("Isolation script cancelled")
        exit(1)

#Activate Script
if __name__ == '__main__':
    token = get_token()
    if(len(Isolation_comment)>0):
        comment = Isolation_comment
        Double_Check()
        response = mdatp_Unisolate_machine(token,comment,)
    else:
        print("No comment added. Isolation cancelled")
        exit(1)
