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

print("Mass Isolation Tool:")
print("\n")

#Obtain machines form CSV
df = pd.read_csv("Machine_list.csv")
machine_df = pd.DataFrame(df['Machine'])

#Isolation Type Selection (Question)
isolation_type_question = [
    inquirer.List('Isolation',message="Select Isolation Type:", choices=["Full","Selective"], default="Selective")
]
isolation_answer = inquirer.prompt(isolation_type_question)

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
def mdatp_isolate_machine(auth_token, comment, isolation_type):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + auth_token
    }

    body = {
        'Comment' : comment,
        'IsolationType' : isolation_type
    }
    for (index, row) in machine_df.iterrows():
        url = "https://api-uk.securitycenter.windows.com/api/machines/"+row['Machine']+"/isolate"
        data = str(json.dumps(body)).encode("utf-8")
        req = urllib.request.Request(url=url,data=data,headers=headers)
        response = urllib.request.urlopen(req)
        jsonResponse = json.loads(response.read())
        if(jsonResponse['status'] == "Pending"):
            print("Isolation of Machine {} initiated".format(row['Machine']))
        else:
            print("Isolation of Machine {} failed".format(row['Machine']))
        

# Final user check
Double_check_question = [
    inquirer.List('Double_check',message="You are going to isolate "+ str(len(machine_df['Machine']))+" machine(s). Are you sure ?", choices=["Yes","No"], default="No")
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
        Isolation_type = isolation_answer['Isolation']
        comment = Isolation_comment
        Double_Check()
        response = mdatp_isolate_machine(token,comment,Isolation_type)
    else:
        print("No comment added. Isolation cancelled")
        exit(1)
