export function rolesPermissionsMapper() {
    //Permissions
    const roleAPermissions: any[] = [];
    const roleBPermissions: any[] = [
        {
            name: "dynamodb",
            accessLevel: "",
            tableName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleCPermissions: any[] = [
        {
            name: "dynamodb",
            accessLevel: "",
            tableName: []
        },
        {
            name: "ssm",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleDPermissions: any[] = [
        {
            name: "dynamodb",
            accessLevel: "",
            tableName: []
        },
        {
            name: "ssm",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "s3",
            accessLevel: "",
            bucket: [],
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleEPermissions: any[] = [
        {
            name: "dynamodb",
            accessLevel: "",
            tableName: []
        },
        {
            name: "ssm",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "s3",
            accessLevel: "",
            bucket: [],
            parameterName: []
        },
        {
            name: "kms",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "states",
            accessLevel: "",
            stateMachine: []
        },
        {
            name: "secretsmanager",
            accessLevel: "read",
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }

    ];
    const roleFPermissions: any[] = [
        {
            name: "ssm",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleGPermissions: any[] = [
        {
            name: "s3",
            accessLevel: "",
            bucket: [],
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleHPermissions: any[] = [
        {
            name: "kms",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleIPermissions: any[] = [
        {
            name: "ssm",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "dynamodb",
            accessLevel: "",
            tableName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        }
    ];
    const roleKPermissions: any[] = [
        {
            name: "dynamodb",
            accessLevel: "",
            tableName: []
        },
        {
            name: "ssm",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "s3",
            accessLevel: "",
            bucket: [],
            parameterName: []
        },
        {
            name: "kms",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "states",
            accessLevel: "",
            stateMachine: []
        },
        {
            name: "secretsmanager",
            accessLevel: "read",
            parameterName: []
        },
        {
            name: "cloudwatch",
            accessLevel: "",
            parameterName: []
        },
        {
            name: "execute-api",
            accessLevel: "",
            parameterName: []
        }

    ];


    const permissionsMapper = new Map();

    permissionsMapper.set("A", roleAPermissions)
    permissionsMapper.set("B", roleBPermissions)
    permissionsMapper.set("C", roleCPermissions)
    permissionsMapper.set("D", roleDPermissions)
    permissionsMapper.set("E", roleEPermissions)
    permissionsMapper.set("F", roleFPermissions)
    permissionsMapper.set("G", roleGPermissions)
    permissionsMapper.set("H", roleHPermissions)
    permissionsMapper.set("I", roleIPermissions)
    permissionsMapper.set("K", roleKPermissions)

    return permissionsMapper

}

export default rolesPermissionsMapper;
