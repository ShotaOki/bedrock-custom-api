import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { Runtime } from "aws-cdk-lib/aws-lambda";

export class StreamBackendStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    /** Lambdaの実行ロールを設定する */
    const role = new cdk.aws_iam.Role(this, "LambdaExecutionRole", {
      assumedBy: new cdk.aws_iam.ServicePrincipal("lambda.amazonaws.com"),
    });
    role.addToPolicy(
      new cdk.aws_iam.PolicyStatement({
        actions: [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "bedrock:*",
        ],
        effect: cdk.aws_iam.Effect.ALLOW,
        resources: ["*"],
      })
    );

    /** Lambdaを作成する */
    const lambdaFunction = new cdk.aws_lambda_nodejs.NodejsFunction(
      this,
      "BedrockStreamingAPI",
      {
        functionName: "BedrockStreamingAPI",
        entry: "functions/stream-api/index.ts",
        runtime: Runtime.NODEJS_18_X,
        timeout: cdk.Duration.seconds(15),
        depsLockFilePath: "package-lock.json",
        bundling: {
          forceDockerBundling: false,
          nodeModules: ["@aws-crypto/crc32", "@aws-sdk/client-bedrock-runtime"],
        },
        role,
      }
    );

    /** 関数URLを公開する */
    lambdaFunction.addFunctionUrl({
      authType: cdk.aws_lambda.FunctionUrlAuthType.AWS_IAM,
      invokeMode: cdk.aws_lambda.InvokeMode.RESPONSE_STREAM,
    });
  }
}
