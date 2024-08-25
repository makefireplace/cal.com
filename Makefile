.PHONY: secret

secret:
	python3 scripts/aws/load_secrets.py
	