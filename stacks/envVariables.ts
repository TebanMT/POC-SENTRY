export function returnEnvVariables(variablesName: string[]) {
    let envVariables: any = {};
    variablesName.forEach((variableName) => {
        if (process.env[variableName] === undefined) {
            throw new Error("Missing environment variable " + variableName);
        }else {
            envVariables[variableName] = process.env[variableName];
        }
    });
    return envVariables;
}