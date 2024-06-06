import * as iam from "aws-cdk-lib/aws-iam";

export function createRoles(stack: any, domainName: string, stageName: string, permissions: any[], typeRole = "lambda") {
    const insights_enabled = String(process.env.LAMBDA_INSIGHTS_ENABLE);
    const principalService = typeRole == "dynamodb"? "apigateway.amazonaws.com" : "lambda.amazonaws.com"
    const actionsPolicy = typeRole == "dynamodb"? "dynamodb:*" : "lambda:InvokeFunction"
    const lambdaRoleGeneralRole = new iam.Role(
        stack,
        typeRole+"Role-domain-" + domainName + "-" + stageName,
        {
            assumedBy: new iam.ServicePrincipal(principalService),
            roleName: typeRole+"Role-domain-" + domainName + "-" + stageName,
        }
    );

    let actions: string[] = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
    ];

    let resources: string[] = ["arn:aws:logs:*:*:*"];

    permissions.forEach((permission: any) => {
        if (permission.name == "dynamodb") {
            if (permission.accessLevel == "read") {
                actions.push("dynamodb:Query");
                actions.push("dynamodb:Scan");
                actions.push("dynamodb:GetItem");
                actions.push("dynamodb:BatchGetItem");
            } else {
                actions.push("dynamodb:Query");
                actions.push("dynamodb:Scan");
                actions.push("dynamodb:GetItem");
                actions.push("dynamodb:BatchGetItem");
                actions.push("dynamodb:PutItem");
                actions.push("dynamodb:UpdateItem");
                actions.push("dynamodb:DeleteItem");
                actions.push("dynamodb:DescribeTable");
            }
            if (permission.tableName.length == 0) {
                resources.push("arn:aws:dynamodb:*:*:table/*");
            } else {
                permission.tableName.forEach((tableName: string) => {
                    resources.push(
                        "arn:aws:dynamodb:*:*:table/" + tableName + "/*"
                    );
                });
            }
        } else if (permission.name == "ssm") {
            if (permission.accessLevel == "read") {
                actions.push("ssm:GetParameter");
                actions.push("ssm:GetParameters");
                actions.push("ssm:GetParametersByPath");
            } else {
                actions.push("ssm:GetParameter");
                actions.push("ssm:GetParameters");
                actions.push("ssm:GetParametersByPath");
                actions.push("ssm:PutParameter");
            }
            if (permission.parameterName.length == 0) {
                resources.push("arn:aws:ssm:*:*:*");
            } else {
                permission.parameterName.forEach((parameterName: string) => {
                    resources.push(
                        "arn:aws:ssm:*:*:parameter/" + parameterName
                    );
                });
            }
        } else if (permission.name == "s3") {
            if (permission.accessLevel == "read") {
                actions.push("s3:GetObject");
            } else {
                actions.push("s3:GetObject");
                actions.push("s3:PutObject");
                actions.push("s3:DeleteObject");
            }
            if (permission.bucket.length > 0) {
                const arn = "arn:aws:s3:::";
                permission.bucket.forEach((bucket: string) => {
                    resources.push(arn + bucket + "/*");
                });
            } else {
                resources.push("arn:aws:s3:::*/*");
                permission.parameterName.forEach((parameterName: string) => {
                    resources.push(
                        "arn:aws:s3:::"+permission.bucket+"/" + parameterName
                    );
                });
            }
        } else if (permission.name == "kms") {
            if (permission.accessLevel == "read") {
                actions.push("kms:DescribeKey");
            } else {
                actions.push("kms:GenerateDataKey");
                actions.push("kms:Decrypt");
                actions.push("kms:DescribeKey");
            }
            if (permission.parameterName.length == 0) {
                resources.push("arn:aws:kms:*:*:key/*");
            } else {
                permission.parameterName.forEach((parameterName: string) => {
                    resources.push(
                        "arn:aws:kms:*"
                    );
                });
            }
        } else if (permission.name == "states") {
            actions.push("states:StartSyncExecution");
            if (permission.stateMachine.length == 0) {
                resources.push("arn:aws:states:*:*:stateMachine:*");
            } else {
                permission.stateMachine.forEach((stateMachine: string) => {
                    resources.push(
                        `arn:aws:states:*:*:stateMachine:${stateMachine}`
                    );
                });
            }
        } else if (permission.name == "secretsmanager") {
            if (permission.accessLevel == "read") {
                actions.push("secretsmanager:GetSecretValue");
            }
            if (permission.parameterName.length == 0) {
                resources.push("arn:aws:secretsmanager:*:*:*");
            } else {
                permission.parameterName.forEach((parameterName: string) => {
                    resources.push(
                        "arn:aws:secretsmanager:*:*:secret/" + parameterName
                    );
                });
            }
        } else if (permission.name == "cloudwatch") {
            actions.push("cloudwatch:PutMetricData");
            resources.push("*");
        } else if (permission.name == "execute-api") {
            actions.push("execute-api:Invoke");
            resources.push("arn:aws:execute-api:*:*:*");
        }
    });


    const lambdaPolicyStatement = new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: actions,
        resources: resources,
    });

    const lambdaPolicy = new iam.Policy(
        stack,
        typeRole+"Policy-domain-" + domainName + "-" + stageName,
        {
            statements: [lambdaPolicyStatement],
        }
    );
    lambdaRoleGeneralRole.attachInlinePolicy(lambdaPolicy);
    const policy = new iam.PolicyStatement({
        actions: [actionsPolicy],
        resources: ["*"]
    })
    lambdaRoleGeneralRole.addToPolicy(policy)
    if(insights_enabled==='True'){
        lambdaRoleGeneralRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('CloudWatchLambdaInsightsExecutionRolePolicy'));
    }

    return lambdaRoleGeneralRole;
}
