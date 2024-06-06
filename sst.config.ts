import { SSTConfig } from "sst";
import { Tags } from "aws-cdk-lib";
import * as process from "process";
import * as cdk from "aws-cdk-lib";
import { RootStack } from "./stacks/RootStack";

export default {
  config(_input: any) {
    const STAGE_NAME = String(process.env.STAGE_NAME || "");
    const AWS_REGION = String(process.env.AWS_REGION || "");
    return {
      name: "hermes2",
      region: AWS_REGION,
      bootstrap: {
        stackName: `${STAGE_NAME}-hermes2-SSTBootstrap`,
      },
    };
  },

  async stacks(app: any) {
    app.setDefaultFunctionProps({
      runtime: "python3.9",
    });

    const stack = new cdk.Stack(app, `${app.stage}-hermes2-RootStack`);
    await RootStack(stack);

    Tags.of(app).add("Project", "Hermes2");
  },
} satisfies SSTConfig;
