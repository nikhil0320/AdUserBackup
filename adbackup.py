import boto3
import sys

customer = sys.argv[1]
regionname = sys.argv[2]

instancename = 'ad-nikhil-new'
command= '.\\ad_backup.ps1'
workingdir ='C:\\temp'
client2 = boto3.client('ssm',regionname)

#params="{"commands":[".\\ad_backup.ps1"],"executionTimeout":["3600"],"workingDirectory":["C:\\temp"]}"

DD_client = boto3.client('dynamodb',regionname)
DD_response = DD_client.scan(TableName='SSM-TEST')
count = DD_response['Count']
count += 1
for client in DD_response['Items']:
   customername = str(client['Client']['S'])
   if customername == customer:
        client1 = str(client['Client']['S'])
        cross_acc_arn = str(client['crossaccount']['S'])
        print cross_acc_arn + "  "+client1
        client = boto3.client('sts')
	role_response = client.assume_role(RoleArn=cross_acc_arn,RoleSessionName='Demo')
	access_key = role_response['Credentials']['AccessKeyId']
	secret_key = role_response['Credentials']['SecretAccessKey']
	session_token = role_response['Credentials']['SessionToken']


	response = client2.send_command(
	    Targets=[
		{
		    'Key': 'tag:Name',
		    'Values': [
			instancename,
		    ]
		},
	    ],
	    DocumentName='AWS-RunPowerShellScript',

	    Parameters={
		'commands': [command],
		'workingDirectory':[workingdir],
		'executionTimeout':['3600']
	    }
	)

	print response
