# aws-instance-auditor
How many instances are running in each region, grouped by name.

This takes inputs of AWS access key and secret key, scans through all AWS regions, and will output the total number in each region, and number of each unique instance name.

**Usage:**  
Can pass in access key/secret key, profile name, or it will use the default profile  
parameters:  
--access-key <key>  
--secret-key <key>
--profile <profile name>  
--verbose  

**Examples:**  
docker run --rm signiant/aws-instance-auditor --access-key=AKIAIOSFODNN7EXAMPLE --secret-key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
docker run --rm -v ~/.aws/credentials:/root/.aws/credentials:ro signiant/aws-instance-auditor --profile=prod --verbose
