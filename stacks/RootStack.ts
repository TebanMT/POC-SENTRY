import { ApiGatewayV1Api } from "sst/constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { CommonStack } from "./commonStack";
import { getOldLayers } from "./layers";
import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";
import * as cdk from "aws-cdk-lib";

export async function RootStack(stack: cdk.Stack) {
  const domainName = process.env["DOMAIN_API"] || undefined;
  const stageName = String(process.env.STAGE_NAME || "");

    const api = new ApiGatewayV1Api(stack, "Api", {
      cdk: {
        restApi: {
          defaultCorsPreflightOptions: {
            allowOrigins: ['"*"'],
          },
        },
      },
    });

    api.cdk.restApi.root.resourceForPath("/api");
    api.attachPermissions(["dynamodb"]);

    // Getting existing layer from Arn
    const layers = getOldLayers(stack);

    new CommonStack(stack, {
      restApiId: api.restApiId,
      rootResourceId: api.cdk.restApi.root.getResource("api")?.resourceId,
      lambdaRuntime: lambda.Runtime.PYTHON_3_9,
      stageName: stageName,
      layers: layers,
      domainName: domainName,
    });

    new cdk.CfnOutput(stack, "ApiEndpoint", {
      value: api.url,
    });

    return {
      apiId: api.restApiId,
      apiRootId: api.cdk.restApi.root.getResource("api")?.resourceId,
    };
}
