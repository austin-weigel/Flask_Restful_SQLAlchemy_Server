from re import A
from flask_restful import abort
import requests

BASE='http://127.0.0.1:5000/'
USER_BASE = BASE + 'user/'
INTEREST_BASE = BASE + 'interest/' 
USER_INTEREST_BASE= BASE + 'userinterest/'
AUSTIN_BASE = USER_BASE + '1'

#Test user data
users = {1:{'username':'austin.weigel', 'email':'austin.a.weigel@gmail.com', 'password':'password123'},
        2:{'username':'kyle.waid', 'email':'kwaid@decksdirect.com', 'password':'password123'},
        3:{'username':'blair.budlong', 'email':'blairb@decksdirect.com', 'password':'password123'}}
#Test interest data
interests = {1:{'title': 'BMX', 'description':'Two wheels for both feet'},
            2:{'title': 'Roller Skating', 'description':'Two front and two rear wheels for each foot'},
            3:{'title': 'Skateboarding', 'description':'Two front and two rear wheels for both feet'},
            4:{'title': 'Unicycling','description':'One wheel for both feet'}}

#Test user_interest data
user_interests = {1:{'user_id':'1','interest_id':'1'},
                2:{'user_id':'2','interest_id':'2'},
                3:{'user_id':'3','interest_id':'3'}}

#Remove user
print(requests.delete(AUSTIN_BASE))
print(requests.get(AUSTIN_BASE).json())
print(requests.put(AUSTIN_BASE, users[1]).json())
print(requests.get(AUSTIN_BASE).json())

#Get user if exists, else put
for user in users:
    url=USER_BASE + str(user)
    data=users[user]
    result = requests.get(url,data)
    if(result.status_code==200):
        print(f'GET user: {result.json()}')
    else:
        print(f'PUT user: {requests.put(url,data).json()}')

#Patch user
print(f'Patch user: {requests.patch(AUSTIN_BASE,{"password":"hired"}).json()}')

#Get interest if exists, else put
for interest in interests:
    url=INTEREST_BASE + str(interest)
    data=interests[interest]
    result = requests.get(url,data)
    if(result.status_code==200):
        print(f'GET interest: {result.json()}')
    else:
        print(f'PUT interest: {requests.put(url,result).json()}, url: {result}')

print(requests.get(USER_INTEREST_BASE +'1/1').json())

#Get user_interest if exists, else put
for user_interest in user_interests:
    user_id = user_interests[user_interest]['user_id']
    interest_id = user_interests[user_interest]['interest_id']
    url= f'{USER_INTEREST_BASE + user_id}/{interest_id}'
    result = requests.get(url)
    if(result.status_code==200):
        print(f'GET user_interest: {result.json()}')
    else:
        print(f'PUT user_interest: {requests.put(url).json()}')