from aws_cdk import App

from src.stack import LighthouseTestStack

app = App()

LighthouseTestStack(app, "LighthouseTestStack")

app.synth()
