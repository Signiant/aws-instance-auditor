import argparse
import boto3


def get_instance_names(session, region_list):
    instance_name_dict = {}
    for region in region_list:
        instance_name_list = []
        client = session.client('ec2', region_name=region)
        try:
            instance_list = client.describe_instances()
        except Exception as e:
            print('Error getting instance details: %s' % e)
            exit(1)

        for instance in instance_list['Reservations']:
            instance_tag_list = instance['Instances'][0]['Tags']
            instance_tags = {}
            for tag in instance_tag_list:
                instance_tags[tag['Key']] = tag['Value']
            if 'Name' in instance_tags:
                instance_name = instance_tags['Name']
            else:
                instance_name = 'No name tag'
            instance_name_list.append(instance_name)
        instance_name_dict[region] = sorted(instance_name_list)
    return instance_name_dict


def list_all_regions(session):
    client = session.client('ec2', region_name='us-east-1')
    try:
        all_ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    except Exception as e:
        print('Error retrieving ec2 regions: %s' % e)
        exit(1)
    return sorted(all_ec2_regions)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get name for all EC2 instances')
    parser.add_argument('--access-key', help='AWS Access Key')
    parser.add_argument('--secret-key', help='AWS Secret Key')
    parser.add_argument('--profile', help='AWS profile')
    parser.add_argument('--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    access_key = None
    secret_key = None
    profile = None
    verbose = None
    total_number_of_instances = 0

    if args.access_key is not None:
        access_key = args.access_key
    if args.secret_key is not None:
        secret_key = args.secret_key
    if args.profile is not None:
        profile = args.profile
    if args.verbose:
        verbose = True

    try:
        if access_key is not None and secret_key is not None:
            session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        elif profile is not None:
            session = boto3.session.Session(profile_name=profile)
        else:
            session = boto3.session.Session()
    except Exception as e:
        print('Error creating boto3 session: %s' % e)
        exit(1)

    if verbose:
        print('Getting list of region names')
    region_list = list_all_regions(session)

    if verbose:
        print('Getting all instances, per region')
    instance_names_per_region = get_instance_names(session, region_list)

    for region in region_list:
        instance_names_in_this_region = instance_names_per_region[region]
        unique_names = sorted(set(instance_names_in_this_region))
        total_number_of_instances += len(instance_names_in_this_region)
        if verbose or len(instance_names_in_this_region) > 0:
            print('\n%s: %s instances' % (region, len(instance_names_in_this_region)))
        for name in unique_names:
            unique_count = '{:3}'.format(instance_names_in_this_region.count(name))
            print(unique_count, name)
    print('Total number of instances: %s' % total_number_of_instances)
