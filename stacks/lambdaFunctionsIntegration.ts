import * as apigateway from "aws-cdk-lib/aws-apigateway";
import {Duration} from "aws-cdk-lib";

export function addLambdaFunctionsIntegration(stack: any, currentResource: any, method: string, cacheEnable: any, lambdaFunction: any, addedOptions: any) {
    const lambdaIntegration = new apigateway.LambdaIntegration(lambdaFunction, {
        proxy: true,
    });

    const method_ = [currentResource.addMethod(method, lambdaIntegration, {
        methodResponses: [
            {
                statusCode: '200',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Origin': true,
                    'method.response.header.Access-Control-Allow-Headers': true,
                    'method.response.header.Access-Control-Allow-Methods': true
                }
            },
            {
                statusCode: '500',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Origin': true,
                    'method.response.header.Access-Control-Allow-Headers': true,
                    'method.response.header.Access-Control-Allow-Methods': true
                }
            },
            {
                statusCode: '400',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Origin': true,
                    'method.response.header.Access-Control-Allow-Headers': true,
                    'method.response.header.Access-Control-Allow-Methods': true
                }
            },
            {
                statusCode: '401',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Origin': true,
                    'method.response.header.Access-Control-Allow-Headers': true,
                    'method.response.header.Access-Control-Allow-Methods': true
                }
            }
        ]
    }), cacheEnable];

    if (!addedOptions[currentResource.path]) {
        const method_options = [currentResource.addMethod('OPTIONS', new apigateway.MockIntegration({
            integrationResponses: [{
                statusCode: '204',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Headers': "'*'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                    'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,GET,PUT,POST,DELETE'",
                },
                responseTemplates: {
                    "application/json": ""
                }
            }],
            passthroughBehavior: apigateway.PassthroughBehavior.NEVER,
            requestTemplates: {
                "application/json": "{\"statusCode\": 200}"
            }
        }), {
            methodResponses: [{
                statusCode: '204',
                responseParameters: {
                    'method.response.header.Access-Control-Allow-Headers': true,
                    'method.response.header.Access-Control-Allow-Methods': true,
                    'method.response.header.Access-Control-Allow-Credentials': true,
                    'method.response.header.Access-Control-Allow-Origin': true,
                }
            }]
        }), true];

        addedOptions[currentResource.path] = true;
        stack.methods.push(method_options);
    }
    stack.methods.push(method_);
}
