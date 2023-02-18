# python-AWS-manager
A command-line interface for interacting with the AWSManager and SSHManager classes.

AWSManager Class
Description:
A class that handles interactions with the Amazon Web Services (AWS) EC2 service using the boto3 Python library.

Properties:
access_key (str): AWS access key.
secret_key (str): AWS secret key.
region (str): AWS region.
session (boto3.session.Session): AWS session object.
ec2 (boto3.client): EC2 client.

Methods:
init(self, access_key=None, secret_key=None, region=None): Constructor method that initializes the class with the provided AWS access key, secret key, and region. Creates a boto3 session and EC2 client object for further interactions with the AWS EC2 service.
create_instance(self, image_id, instance_type, min_count, max_count, key_name): Method that creates a new EC2 instance with the provided image ID, instance type, minimum and maximum instance counts, and key pair name. Returns the ID of the new instance.
describe_instances(self): Method that retrieves and prints information about all running instances in the AWS account.
stop_instance(self, instance_id): Method that stops the instance with the provided ID.
terminate_instance(self, instance_id): Method that terminates the instance with the provided ID.
get_public_ip(self, instance_id): Method that retrieves the public IP address of the instance with the provided ID.

SSHManager Class
Description:
A class that handles SSH connections to a remote machine using the paramiko Python library.

Properties:
host (str): IP address or hostname of the remote machine.
username (str): Username to use for the SSH connection.
key_file (str): Path to the private key file for the SSH connection.
ssh (paramiko.SSHClient): SSH client object.
Methods:
init(self, host, username, key_file): Constructor method that initializes the class with the provided remote machine IP address or hostname, username, and private key file. Creates a paramiko SSH client object for further interactions with the remote machine.
connect(self): Method that establishes the SSH connection to the remote machine.
run_command(self, command): Method that runs the provided command on the remote machine and prints the output to the console.
transfer_file(self, local_file, remote_file): Method that transfers the file at the provided local path to the provided remote path on the remote machine using SFTP.
Main Program
Description:
A command-line interface for interacting with the AWSManager and SSHManager classes.

Usage:
The program prompts the user for AWS credentials and region on startup. The user can then choose from the following options:

Create a new EC2 instance
Describe existing EC2 instances
Stop an EC2 instance
Terminate an EC2 instance
Retrieve public IP address of an instance
Copy files to an instance using SFTP
Run a command on an instance
To quit the program, the user can enter "Q" at any time.



