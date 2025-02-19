install:
	uv sync

bootstrap:
	cdk bootstrap

deploy:
	uv export --all-extras --no-dev -o src/requirements.txt -q
	cdk deploy

destroy:
	cdk destroy

test:
	uv run pytest ./tests
