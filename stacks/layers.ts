import { Stack } from "aws-cdk-lib/core";
import * as lambda from "aws-cdk-lib/aws-lambda";


export function getUtilsLayer(stack: Stack) {
    const versionUtilsLayerArn = String(process.env.ARN_LAYER_UTILS || "");
    return lambda.LayerVersion.fromLayerVersionArn(stack, "utilsLayerArn", 'arn:aws:lambda:us-east-1:933334258191:layer:estebanLayerTest:67');
}

export function getAuthenticationLayer(stack: Stack) {
    const versionAuthenticationLayerArn = String(process.env.ARN_LAYER_AUTHENTICATION || "");
    return lambda.LayerVersion.fromLayerVersionArn(stack, "authenticationLayerArn", 'arn:aws:lambda:us-east-1:933334258191:layer:estebanExternalLibrariesTest:3');
}

export function getZeepLayer(stack: Stack) {
    const versionZeepLayerArn = String(process.env.ARN_LAYER_PYTHON39_X86_64_ZEEP || "");
    return lambda.LayerVersion.fromLayerVersionArn(stack, "zeepLayerArn", versionZeepLayerArn);
}


export function getOldLayers(stack: Stack) {
    return [
        getZeepLayer(stack)
    ];
}