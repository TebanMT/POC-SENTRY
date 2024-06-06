export function addResourceApiGateway(api: any, path: string) {
    const pathSegments = path
        .split("/")
        .filter((segment) => segment !== "");
    let currentResource = api.root;
    for (const part of pathSegments) {
        if (part.trim() !== "") {
            let res = currentResource.resourceForPath(part);
            if (res === undefined) {
                res = currentResource.addResource(part);
            }
            currentResource = res;
        }
    }
    return currentResource
}