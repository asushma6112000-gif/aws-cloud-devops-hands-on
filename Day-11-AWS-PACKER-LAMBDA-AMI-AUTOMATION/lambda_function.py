import boto3

target_regions = ["us-east-1", "ap-southeast-2"]


def lambda_handler(event, context):

    print("Received event:")
    print(event)

    ami_id = event["detail"]["responseElements"]["imageId"]
    ami_name = event["detail"]["requestParameters"]["name"]
    source_region = event["region"]

    print(f"AMI ID: {ami_id}")
    print(f"AMI Name: {ami_name}")
    print(f"Source Region: {source_region}")

    if "goldem-image" not in ami_name:
        print("Not target AMI")
        return "Not target AMI"

    for region in target_regions:

        print(f"Copying AMI to {region}")

        ec2 = boto3.client(
            "ec2",
            region_name=region
        )

        response = ec2.copy_image(
            SourceRegion=source_region,
            SourceImageId=ami_id,
            Name=f"{ami_name}-copy-{region}"
        )

        print(f"Copy started in {region}")
        print(f"New AMI ID: {response['ImageId']}")

    print("AMI copy started successfully")

    return "AMI copy started successfully"
