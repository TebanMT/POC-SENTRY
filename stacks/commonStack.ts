import * as apigateway from "aws-cdk-lib/aws-apigateway";
import {NestedStack} from "aws-cdk-lib/core";
import {ResourceNestedStackProps} from "./Stacksinterface"
import {Construct} from 'constructs';
import {Method} from "aws-cdk-lib/aws-apigateway";
import * as lambda from 'aws-cdk-lib/aws-lambda';
import {DeployStack} from "./DeployStacks";
import {rolesPermissionsMapper} from './rolesPermissions';
import {createRoles} from "./lambdaResources";
import {createLambdaFunctions} from "./lambdaFunctions";
import {returnEnvVariables} from "./envVariables";
import {createLambdaLogGroup} from "./logGroups";
import {addResourceApiGateway} from "./resourcesIntegration";
import {addLambdaFunctionsIntegration} from "./lambdaFunctionsIntegration";
import { getAuthenticationLayer, getUtilsLayer, getZeepLayer} from "./layers";

export class CommonStack extends NestedStack {
    public readonly methods: Method[] = [];

    constructor(scope: Construct, props: ResourceNestedStackProps) {
        
        super(scope, 'integ-restapi-import-common', props);

        const stageName = String(process.env.STAGE_NAME || "");
        const logGroup = createLambdaLogGroup(this, props.stageName, "common-stack");

        const utilsLayer = getUtilsLayer(this);
        const authenticationLayer = getAuthenticationLayer(this);
        const zeepLayer = getZeepLayer(this);

        const api = apigateway.RestApi.fromRestApiAttributes(this, 'RestApi', {
                restApiId: props.restApiId,
                rootResourceId: props.rootResourceId,
        });




        const permissionsMapper = rolesPermissionsMapper()
        //Roles
        const roleC = createRoles(this, "roleC", stageName, permissionsMapper.get("C"))


        const envVarsCompliace = returnEnvVariables(['LEGACY_FRONT_OFFICE1', 'LEGACY_FRONT_OFFICE2',
            'ACCESS_CONTROL_ALLOW_ORIGIN','ENVIRONMENT_VAR',
            'BASE_API_REST_HERMES1', 'TTL_DYNAMO_RECORDS']);

            const new_props =  {...props};
            new_props.layers= [ utilsLayer, authenticationLayer, zeepLayer];

        // Common Lambdas
        const lambdaFunction = createLambdaFunctions(
               this, api, "TestSentry",
               "sentry.test",
               "services/functions/handlers/sentry",
               stageName, envVarsCompliace, roleC, logGroup, new_props
         );

        const resource = addResourceApiGateway(api, 'test')
        addLambdaFunctionsIntegration(this, resource, 'GET', false, lambdaFunction, {})





        new DeployStack(this, {
            restApiId: api.restApiId,
            methods: this.methods,
            stageName: props.stageName,
            domainName: props.domainName
        });

    }

}
