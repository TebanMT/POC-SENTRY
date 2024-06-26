
import { NestedStack } from "aws-cdk-lib/core";
import { DeployStackProps } from "./Stacksinterface";
import { Construct } from 'constructs';
import { RestApi, Stage, Deployment, PassthroughBehavior } from 'aws-cdk-lib/aws-apigateway';
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as logs from "aws-cdk-lib/aws-logs";
import {Duration} from "aws-cdk-lib";
import {returnEnvVariables} from "./envVariables";

export class DeployStack extends NestedStack {
  constructor(scope: Construct, props: DeployStackProps) {
    super(scope, 'integ-restapi-import-DeployStack', props);

    const envVars = returnEnvVariables(['CACHE_CLUSTER_SIZE', 'CACHE_TTL']);
    const cacheClusterSize = '0.5';
    const cacheTtl = envVars['CACHE_TTL'];

    const api = RestApi.fromRestApiId(this, 'RestApi', props.restApiId)
    const deployment = new Deployment(this, 'Deployment' + Date.now().toString(), {
      api: api,
    });
    const logGroup = new logs.LogGroup(this, 'ApiLogs');
    let methodOptionsDict = {};

    if (props.methods) {
      for (let item of props.methods) {
        let method = item[0]
        let cacheVariable = item[1]

        if (method) {
          const resource_ = method.resource.path;
          const method_ = method.httpMethod;

          if (cacheVariable) {
              methodOptionsDict[`/api${resource_}/${method_}`] = {
                cachingEnabled: true,
                cacheTtl: Duration.minutes(cacheTtl)
              }
              deployment.node.addDependency(method);
            } else {
              methodOptionsDict[`/api${resource_}/${method_}`] = {
                cachingEnabled: false
              }
            }
        };
      }
    }


    const stage = new Stage(this, 'Stage', {
      deployment,
      accessLogDestination: new apigateway.LogGroupLogDestination(logGroup),
      stageName: props.stageName+'-',
      tracingEnabled: true,
      methodOptions: methodOptionsDict
    });

    if ((["qa", "dev", "staging", "hotfix", "bugfix"].includes(props.stageName))){
      const domain = apigateway.DomainName.fromDomainNameAttributes(this, props.stageName+'CustomDomain', {
        domainName: props.domainName!,
        domainNameAliasTarget: "",
        domainNameAliasHostedZoneId: "",
      });
      new apigateway.BasePathMapping(this, props.stageName+'BasePathMapping', {
        domainName: domain,
        restApi: api,
        stage: stage,
      });

    }

  }
}
