# scripts used to generate a new bucket and user for the object store

import boto3
import os
import botocore
# import botocore.exceptions
import json
import sys

# # gives a response but don't think can use it.

# iam = boto3.client('iam')
# response = iam.create_user(UserName='rfc-cap-feed')
# response = iam.create_access_key(UserName='rfc-cap-feed')
# print(response)

class admin_bucket_access():

    def __init__(self):
        self.obj_store_user = os.getenv('OBJ_STORE_USER')
        self.obj_store_secret = os.getenv('OBJ_STORE_SECRET')
        self.obj_store_host = os.getenv('OBJ_STORE_HOST')
        self.client = self.create_client()
        
    def create_client(self):
        boto_session = boto3.session.Session()
        boto_client = boto_session.client(
                    service_name="s3",
                    aws_access_key_id=self.obj_store_user,
                    aws_secret_access_key=self.obj_store_secret,
                    endpoint_url=f"https://{self.obj_store_host}",
                )
        return boto_client
    
    def get_user_arn(self, user):
        iam = boto3.client('iam')
        get_user_resp = iam.get_user(
            UserName=user
        )
        print("response from get user: ", get_user_resp)
        return get_user_resp['User']['Arn']
    
    def bucket_exists(self, bucket_name):
        bucket_exists = False
        resp = self.client.list_buckets()
        bucket_names = []
        for bucket_info in resp['Buckets']:
            bucket_names.append(bucket_info['Name'])
        if bucket_name in bucket_names:
            bucket_exists = True
        return bucket_exists

    def create_bucket(self, bucket_name):
        if not self.bucket_exists(bucket_name):
            self.client.create_bucket(Bucket=bucket_name)
    
    def user_exists(self, user):
        iam = boto3.client('iam')
        resp = iam.list_users()
        users =  []
        for cur_user in resp['Users']:
            users.append(cur_user['UserName'])
        if user in users:
            return True
        else:
            return False

    def delete_user(self, user):
        iam = boto3.client('iam')
        if self.user_exists(user):
            acc_keys = iam.list_access_keys(
                UserName=user
            )
            for acc_key in acc_keys['AccessKeyMetadata']:
                response = iam.delete_access_key(
                    UserName=user,
                    AccessKeyId=acc_key['AccessKeyId']
                )
            iam.delete_user(UserName=user)

    def create_user(self, user):
        iam = boto3.client('iam')
        if not self.user_exists(user):
            resp = iam.create_user(UserName=user)
            print("resp from create user: ", resp)
            response = iam.create_access_key(UserName=user)
            print("resp from create access key: ", response)
    

    def bucket_policy_exists(self, bucket_name, bucket_policy_name):
        policy_exists = False
        resp = None
        try:
            resp = self.client.get_bucket_policy(
                Bucket=bucket_name,
                ExpectedBucketOwner=self.obj_store_user)
            print("resp from get bucket policy: ", resp)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                print("No such bucket policy exists")
            else:
                raise
        if resp:
            policy_exists = True
        return policy_exists
    
    def delete_bucket_policy(self, user, bucket_name, bucket_policy):
        if self.bucket_policy_exists(bucket_name=bucket_name, bucket_policy_name=bucket_policy):
            self.client.delete_bucket_policy(
                Bucket=bucket_name
            )
    
    def give_user_bucket_access(self, user, bucket_name, bucket_policy):
        if not self.bucket_policy_exists(bucket_name, bucket_policy):
            user_arn = self.get_user_arn(user)
            print("user arn: ", user_arn)

            bucket_policy_spec = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": bucket_policy,
                        "Effect": "Allow",
                        "Principal": user,
                        "Action": [
                            "s3:*"
                        ],
                        "Resource": [
                            f"arn:aws:s3:::{bucket_name}"
                        ]
                    }
                ]
            }
            self.client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(bucket_policy_spec)
            )

    def get_bucket_policy(self, bucket_name, expected_bucket_owner):
        # needs a try except block
        resp = self.client.get_bucket_policy(
            Bucket=bucket_name,
            ExpectedBucketOwner=expected_bucket_owner
        )
        return resp

            




if __name__ == '__main__':
    bucket_name = 'rfc-cap-feed'
    user = 'rfc-cap-feed-user'
    bucket_policy_name = 'RFCCapBucketAccess'
    bucket_administrator = admin_bucket_access()

    bucket_administrator.get_bucket_policy(bucket_name=bucket_name, expected_bucket_owner=bucket_administrator.obj_store_user)
    #bucket_administrator.create_bucket(bucket_name=bucket_name)
    #bucket_administrator.delete_user(user=user)
    #bucket_administrator.create_user(user=user)
    #bucket_administrator.delete_bucket_policy(user=user, bucket_name=bucket_name, bucket_policy=bucket_policy_name)
    #bucket_administrator.give_user_bucket_access(user=user, bucket_name=bucket_name, bucket_policy=bucket_policy_name)
