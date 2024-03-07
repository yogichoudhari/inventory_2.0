from decouple import config
from django.core.cache import cache
from payment.services import assign_subscription_to_user
from user.models import User as CustomUser,Role
from django.contrib.auth.models import User
from payment.services import assign_subscription_to_user
from user.services import create_stripe_customer
from inventory_management_system.utils import send_email
import requests
import urllib.parse
import logging
import pdb
import time
import stripe



logger = logging.getLogger('watchtower')
CLIENT_ID = config('SALESFORCE_CLIENT_ID')
CLIENT_SECRET = config('SALESFORCE_CLIENT_SECRET')
REDIRECT_URI = config("SALESFORCE_REDIRECT_URI")
base_url = "https://webkorps5-dev-ed.develop.my.salesforce.com"

# Function to get authorization dialog URL
def get_auth_dialog_url():
   # Combine base URL, authorization endpoint, response type, redirect URI, and client ID
   url = f"{base_url}/services/oauth2/authorize?response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}"
   return url  # Return the generated URL

def get_access_token(code):
    headers = {
               "content-type": "application/json"
               }
    
    payload = {
        'grant_type':'authorization_code',
        'code':code,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        'redirect_uri':'https://localhost:8000/api/salesforce/oauth/callback'
    }
    access_tokenn_url = f"{base_url}/services/oauth2/token"
    pdb.set_trace()
    response = requests.post(access_tokenn_url,params=payload,headers=headers)
    return response.json()
    
def fetch_salesforce_users(admin_user):
    try:
        endpoint ="/services/data/v59.0/chatter/users/"
        url = f'{base_url}{endpoint}'
        access_token = cache.get('salesforce_access_token')
        headers = {'Authorization':f"Bearer {access_token}"}
        response = requests.get(url,headers=headers)
        
        if response.status_code==200:
            process_salesforce_users(admin_user,response)
            
        elif response.status_code==401:
            new_acccess_token = refresh_access_token()
            cache.set("salesforce_access_token",new_acccess_token)
            
    except Exception as e :
        template_name = "salesforce_user.html"
        subject= "Salesforce user synchronization in Application"
        email = admin_user.user.email
        context = {"error":f'{str(e)}',"admin":admin_user}
        send_email(context,email,template_name,subject)
        logger.error(f'error occured while updating the user as {str(e)}')


def refresh_access_token():
    pdb.set_trace()
    refresh_access_token_url = f"{base_url}/services/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': cache.get("salesforce_refresh_token")
    }
    response = requests.post(url=refresh_access_token_url,data=data,headers=headers)
    if response.status_code==200:
       return response.json().get('access_token')
    else:
        logger.info(f"something went wrong: {str(response.json())}")


def process_salesforce_users(admin_user,response):
    users = response.json()['users']
    role = Role.objects.get(name='Customer')
    account = admin_user.account
    users_arr = []
    for user in users:
        if check_valid_user(user):
            user_obj = create_user_from_salesforce_users(user,role,account)
            users_arr.append(user_obj)
    if users_arr:
        subject= "Salesforce user synchronization in Application"
        email = admin_user.user.email
        context = {"users":users_arr,"admin":admin_user}
        template_name = "salesforce_user.html"
        send_email(context,email,template_name,subject)
    else:
        logger.info(f'Users are up to date updated')
        
        

def check_valid_user(user):
    if ( user['email'] not in ['noreply@example.com','yogesh.choudhari@webkorps.com'] 
        and user['email'] not in [user.email for user in User.objects.all()]):
        return True
    else:
        return False

def create_user_from_salesforce_users(user_data,role,account):
    username = user_data.get('username', '')
    first_name = user_data.get('firstName', '')
    last_name = user_data.get('lastName', '')
    phone = user_data.get('phoneNumbers', [''])[0]
    email = user_data.get('email', '')
    address = user_data.get('address', {})
    
    base_user_obj = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
    base_user_obj.set_password('123456')
    base_user_obj.save()
    
    user = CustomUser.objects.create(
        user=base_user_obj,
        phone=phone,
        account=account,
        role=role,
        city=address.get('city', ''),
        state=address.get('state', ''),
        is_verified=True
    )
    
    user_stripe_id = create_stripe_customer(user)
    user.stripe_id = user_stripe_id
    _,subscription_instance = assign_subscription_to_user(user,"monthly","Standard")
    user.subscription = subscription_instance
    user.save()
    user_dict = {}
    user_dict.update({"username":username,'first_name':first_name,"last_name":last_name,"email":email})
    return user_dict

            
                        
    


    
