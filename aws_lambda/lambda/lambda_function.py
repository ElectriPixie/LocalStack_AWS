import boto3

def lambda_handler(event, context):
    apigateway = boto3.client('apigateway')

    # Get the REST API ID
    rest_api_response = apigateway.get_rest_apis()
    if not rest_api_response['items']:
        return {
            'statusCode': 500,
            'body': 'No REST API found'
        }

    rest_api_id = rest_api_response['items'][0]['id']

    # Get the resources (endpoints)
    resources_response = apigateway.get_resources(restApiId=rest_api_id)  # ✅ Corrected parameter name
    resource_id = None

    # Find the resource with a GET method (adjust as needed)
    for resource in resources_response['items']:
        if 'GET' in resource.get('resourceMethods', {}):
            resource_id = resource['id']
            break

    if not resource_id:
        return {
            'statusCode': 500,
            'body': 'No resource with GET method found'
        }

    # Get integration details
    try:
        integration_response = apigateway.get_integration(
            restApiId=rest_api_id,
            resourceId=resource_id,
            httpMethod='GET'
        )
    except apigateway.exceptions.NotFoundException:
        return {
            'statusCode': 500,
            'body': 'Integration not found'
        }

    # Update integration using patch operations
    apigateway.update_integration(
        restApiId=rest_api_id,
        resourceId=resource_id,
        httpMethod='GET',
        patchOperations=[
            {
                'op': 'replace',
                'path': '/requestTemplates/application~1json',
                'value': '{"statusCode": 200}'
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': 'Integration updated successfully',
    }