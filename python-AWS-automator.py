import boto3
import paramiko

class AWSManager:
    def __init__(self, access_key=None, secret_key=None, region=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )
        self.ec2 = self.session.client('ec2')

    def create_instance(self, image_id, instance_type, min_count, max_count, key_name):
        response = self.ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            MinCount=int(min_count),
            MaxCount=int(max_count),
            KeyName=key_name
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f'Created instance {instance_id}')
        return instance_id

    def describe_instances(self):
        response = self.ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f'Instance ID: {instance["InstanceId"]}, State: {instance["State"]["Name"]}')

    def stop_instance(self, instance_id):
        self.ec2.stop_instances(InstanceIds=[instance_id])
        print(f'Stopped instance {instance_id}')

    def terminate_instance(self, instance_id):
        self.ec2.terminate_instances(InstanceIds=[instance_id])
        print(f'Terminated instance {instance_id}')

    def get_public_ip(self, instance_id):
        response = self.ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(f'Public IP address of instance: {public_ip}')
        return public_ip

class SSHManager:
    def __init__(self, host, username, key_file):
        self.host = host
        self.username = username
        self.key_file = key_file
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.ssh.connect(self.host, username=self.username, key_filename=self.key_file)

    def run_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        if error:
            print(f'Error: {error}')
        else:
            print(output)

    def transfer_file(self, local_file, remote_file):
        sftp = self.ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        print(f'Copied {local_file} to {remote_file}')

# Prompt user for AWS credentials and region
access_key = input('Enter your AWS access key: ')
secret_key = input('Enter your AWS secret key: ')
region = input('Enter the region you want to connect to (e.g. us-east-1): ')

# Create AWSManager object
aws_manager = AWSManager(access_key, secret_key, region)

# Prompt user to choose an option
while True:
    print('\nChoose an option:\n1. Create a new EC2 instance\n2. Describe existing EC2 instances\n3. Stop an EC2 instance\n4. Terminate an EC2 instance\n5. Retrieve public IP address of an instance\n6. Copy files to an instance using SFTP\n7. Run a command on an instance\n')
    print('Q. Quit\n')

    option = input('Option: ')

    if option == '1':
        # Prompt user for instance details
        image_id = input('Enter the ID of the AMI you want to use: ')
        instance_type = input('Enter the instance type (e.g. t2.micro): ')
        min_count = input('Enter the minimum number of instances to launch: ')
        max_count = input('Enter the maximum number of instances to launch: ')
        key_name = input('Enter the name of the key pair to use: ')

        # Create the instance
        aws_manager.create_instance(image_id, instance_type, min_count, max_count, key_name)

    elif option == '2':
        # Describe existing instances
        aws_manager.describe_instances()

    elif option == '3':
        # Prompt user for instance ID
        instance_id = input('Enter the ID of the instance you want to stop: ')

        # Stop the instance
        aws_manager.stop_instance(instance_id)

    elif option == '4':
        # Prompt user for instance ID
        instance_id = input('Enter the ID of the instance you want to terminate: ')

        # Terminate the instance
        aws_manager.terminate_instance(instance_id)

    elif option == '5':
        # Prompt user for instance ID
        instance_id = input('Enter the ID of the instance you want to retrieve the public IP address of: ')

        # Retrieve the public IP address
        public_ip = aws_manager.get_public_ip(instance_id)
        print(f'Public IP address of instance {instance_id}: {public_ip}')

    elif option == '6':
        # Prompt user for SSH details
        host = input('Enter the public IP address of the instance: ')
        username = input('Enter the username to log in as: ')
        key_file = input('Enter the path to the private key file: ')
        local_file = input('Enter the path to the local file to copy: ')
        remote_file = input('Enter the path to the remote destination: ')

        # Transfer the file using SFTP
        ssh_manager = SSHManager(host, username, key_file)
        ssh_manager.connect()
        ssh_manager.transfer_file(local_file, remote_file)

    elif option == '7':
        # Prompt user for SSH details
        host = input('Enter the public IP address of the instance: ')
        username = input('Enter the username to log in as: ')
        key_file = input('Enter the path to the private key file: ')
        command = input('Enter the command to run: ')

        # Run the command on the instance
        ssh_manager = SSHManager(host, username, key_file)
        ssh_manager.connect()
        ssh_manager.run_command(command)

    elif option.lower() == 'q':
        # Exit the program
        break

    else:
        # Invalid option
        print('Invalid option. Please choose again.')
