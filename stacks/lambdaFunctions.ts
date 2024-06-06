import * as lambda from "aws-cdk-lib/aws-lambda";
import {Duration} from "aws-cdk-lib";
import {ServicePrincipal} from "aws-cdk-lib/aws-iam";
import {LogGroup} from "aws-cdk-lib/aws-logs";
export function createLambdaFunctions(stack: any, api: any, lambdaName: string, handler: string, codeAsset: string, stageName: string, envVars: any, role: any, logGroup: LogGroup, props: any, memorySize: number = 1024, timeout: number = 60) {

    const idLambda = (stageName + "-" + lambdaName)

    const lambdaFunction = new lambda.Function(stack, idLambda, {
        runtime:            props.lambdaRuntime,
        handler:            handler,
        environment:        envVars,
        code:               lambda.Code.fromAsset(codeAsset),
        layers:             props.layers,
        role:               role,
        timeout:            Duration.seconds(timeout),
        logGroup:           logGroup,
        insightsVersion:    lambda.LambdaInsightsVersion.VERSION_1_0_143_0,
        functionName:       idLambda,
        memorySize:         memorySize
    });
    lambdaFunction.addPermission('PermitionInvocation', {
        principal: new ServicePrincipal('apigateway.amazonaws.com'),
        sourceArn: api.arnForExecuteApi('*')
    });

    return lambdaFunction;
}
