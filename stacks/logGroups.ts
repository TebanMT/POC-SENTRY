import { Construct } from "constructs";
import * as cdk from "aws-cdk-lib"
import * as logs from "aws-cdk-lib/aws-logs";


export const createLogGroup = (scope: Construct, id: string, name: string) : logs.LogGroup => {
    return new logs.LogGroup(scope, id, {
        logGroupName : name,
        retention: parseInt(process.env.LOG_RETENTION_DAYS ?? `${logs.RetentionDays.ONE_MONTH}`),
        removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
};


export const createLambdaLogGroup = (scope: Construct, stageName: string, domainName: string) : logs.LogGroup => {
    return createLogGroup(
        scope,
        `log-lambda-${stageName}-${domainName}`,
        `/aws/lambda/hermes2/${stageName}/${domainName}`
    )
};


export const createStepFunctionLogGroup = (scope: Construct, stageName: string, domainName: string) : logs.LogGroup => {
    return createLogGroup(
        scope,
        `log-step-function-${stageName}-${domainName}`,
        `/aws/vendedlogs/hermes2/${stageName}/${domainName}`
    )
};
