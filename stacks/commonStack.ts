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
import {Duration} from "aws-cdk-lib";
import {createLambdaLogGroup} from "./logGroups";
import {addResourceApiGateway} from "./resourcesIntegration";
import {addLambdaFunctionsIntegration} from "./lambdaFunctionsIntegration";
import { getAuthenticationLayer, getUtilsLayer, getZeepLayer} from "./layers";

export class CommonStack extends NestedStack {
    public readonly methods: Method[] = [];

    constructor(scope: Construct, props: ResourceNestedStackProps) {
        
        super(scope, 'integ-restapi-import-common', props);

        const stageName = String(process.env.STAGE_NAME || "");
        const environment_var = String(process.env.ENVIRONMENT_VAR || "");
        const cache_duration = String(process.env.CACHE_TIME || 0); // CITIES ENVS
        const password_es_cities = String(process.env.PASSWORD_ES_CITIES || "");
        const access_allow_origin = String(
            process.env.ACCESS_CONTROL_ALLOW_ORIGIN || "*"
        );
        const base_api_rest_keycloak = String(
            process.env.BASE_API_REST_KEYCLOAK || ""
        );
        const realm_keycloak = String(process.env.REALM_KEYCLOAK || "");
        const insights_enabled = String(process.env.INSIGHTS_ENABLED)
        const contactTableEnv = String(process.env.HERMES2_CONTACT_TABLE_ENV)
        const baseUrlElastichSearchCustomer = String(process.env.BASE_URL_ELASTICSEARCH_SEARCH_CUSTOMER)

        const environment = {
            STAGE_NAME: stageName,
            PASSWORD_ES_CITIES: password_es_cities,
            ACCESS_CONTROL_ALLOW_ORIGIN: access_allow_origin,
            BASE_API_REST_KEYCLOAK: base_api_rest_keycloak,
            REALM_KEYCLOAK: realm_keycloak,
            ENVIRONMENT_VAR: environment_var,
            HERMES2_CONTACT_TABLE_ENV: contactTableEnv,
            BASE_URL_ELASTICSEARCH_SEARCH_CUSTOMER: baseUrlElastichSearchCustomer
        };

        const logGroup = createLambdaLogGroup(this, props.stageName, "common-stack");

        const utilsLayer = getUtilsLayer(this);
        const authenticationLayer = getAuthenticationLayer(this);
        const zeepLayer = getZeepLayer(this);

        const api = apigateway.RestApi.fromRestApiAttributes(this, 'RestApi', {
                restApiId: props.restApiId,
                rootResourceId: props.rootResourceId,
        });

        const lambdaFunctionAuthorizer = new lambda.Function(this, stageName + "-AuthorizerFunction", {
            runtime: props.lambdaRuntime,
            handler: "api_gateway_authorizer.authorizer",
            environment: environment,
            code: lambda.Code.fromAsset("services/functions/handlers/sentry"),
            layers: [utilsLayer, authenticationLayer ],
            timeout: Duration.seconds(60),
            logGroup : logGroup,
            insightsVersion: lambda.LambdaInsightsVersion.VERSION_1_0_143_0,
        });
        const authorizer = new apigateway.TokenAuthorizer(
            this,
            stageName + "-Hermes20Auth",
            {
                authorizerName: stageName + "-keycloakAuthorizer",
                handler: lambdaFunctionAuthorizer,
                identitySource: apigateway.IdentitySource.header("Authorizer"),
                resultsCacheTtl: Duration.seconds(Number(cache_duration)),
            }
        );

        authorizer._attachToApi(api)




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
        addLambdaFunctionsIntegration(this, resource, 'GET', false, lambdaFunction, authorizer, {})





        new DeployStack(this, {
            restApiId: api.restApiId,
            methods: this.methods,
            stageName: props.stageName,
            domainName: props.domainName
        });

    }

}
