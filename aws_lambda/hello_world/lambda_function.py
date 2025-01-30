import boto3

def lambda_handler(event, context):
    apigateway = boto3.client('apigateway')

    # Get the REST API ID
    rest_api_response = apigateway.get_rest_apis()
    rest_api_id = rest_api_response['items'][0]['id']

    # Get the integration ID
    integration_response = apigateway.get_integration(
        RestApiId=rest_api_id,
        MethodName='GET'
    )
    integration_id = integration_response['id']

    # Use the integration ID to update the integration
    updated_integration_response = apigateway.update_integration(
        RestApiId=rest_api_id,
        ResourceId=integration_id,
        MethodName='GET',
        HttpMethod='GET',
        RequestParameters={},
        RequestTemplates={},
        Responses=[{}],
        Uri='lambda:lambda_function_name',
        IntegrationType='LAMBDA',
        RequestParameters={},
        RequestTemplates={},
        Responses=[{}]
    )

    return {
        'statusCode': 200,
        'body': 'Integration updated successfully',
    }