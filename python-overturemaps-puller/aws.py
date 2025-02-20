import boto3
import json

def set_aws_credentials(aws_access_key_id, aws_secret_access_key):
    # Create a session with the provided credentials 
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1'
    )
    # Use the session to interact with AWS services
    client = session.client('secretsmanager')
    # Now you can use the client to retrieve secrets, etc.
    return client

def get_secret(config, secret_name):
    #get relevant config fields
    aws_credentials = config['aws_creds']
    city_alias = config['city_alias']

    #retrieve secret with value
    client = set_aws_credentials(aws_credentials['aws_access_key_id'], aws_credentials['aws_secret_key'])
    secret = client.get_secret_value(SecretId = f'cities/{city_alias}/{secret_name}')
    return secret

