import { NestedStackProps, listMapper } from "aws-cdk-lib/core";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { Role } from "aws-cdk-lib/aws-iam";

export interface ResourceNestedStackProps extends NestedStackProps {
    readonly restApiId: string;
    readonly rootResourceId: string | undefined;
    readonly lambdaRuntime: string;
    readonly stageName: string;
    readonly authorizer: apigateway.TokenAuthorizer;
    readonly layers: any[];
    readonly role: Role;
    readonly dynamoRole?: Role;
    readonly domainName?: string;
    readonly provisionedLambdas?: { [key: string]: any };
  }

  export interface DeployStackProps extends NestedStackProps {
    readonly restApiId: string;
    readonly methods?: Method[];
    readonly stageName: string;
    readonly domainName: string | undefined;
  }
