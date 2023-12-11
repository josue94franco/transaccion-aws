from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    #aws_ses as ses,
    # aws_sqs as sqs,
)
from constructs import Construct

class TransaccionAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # definicion de función lambda   
        ft = _lambda.Function(self, "func_transaccion", function_name="func_transaccion",
                                 runtime=_lambda.Runtime.PYTHON_3_9,
                                 handler="handler.handler",
                                 code=_lambda.Code.from_asset("./Lambdas")
                                                                 
                                )
        
        
        # Política IAM para permitir el envío de correos a través de SES
        ses_policy = iam.PolicyStatement(
            actions=['ses:SendEmail', 'ses:SendRawEmail'],
            resources=['*'] 
        )

        # Añade la política al rol de la función Lambda
        ft.add_to_role_policy(ses_policy)
