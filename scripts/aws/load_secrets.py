import boto3
from botocore.exceptions import ClientError
import os
import json
import shutil


def get_secret(env: str) -> str:
    if env != "dev" and env != "prod":
        raise ValueError('Invalid environment. Must be "dev" or "prod".')

    secret_name = env + "/cal.com"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        print("Fetching secrets...")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    return get_secret_value_response["SecretString"]


def convert_to_dict(json_string: str) -> dict:
    return json.loads(json_string)


def write_to_env_file(config: dict, env_file: str, example_env_file: str) -> None:
    shutil.copy2(example_env_file, env_file)

    with open(env_file, "r") as f:
        lines = f.readlines()

    updated_lines = []
    keys_found = set()

    for line in lines:
        if "=" in line:
            key, _ = line.split("=", 1)
            key = key.strip()
            if key in config:
                updated_lines.append(f"{key}={config[key]}\n")
                keys_found.add(key)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # Append any new keys from config that weren't in the original file
    for key, value in config.items():
        if key not in keys_found:
            updated_lines.append(f"{key}={value}\n")

    with open(env_file, "w") as f:
        f.writelines(updated_lines)

    print("Success")


def write_to_env_appstore_file(env_file: str, example_env_file: str) -> None:
    shutil.copy2(example_env_file, env_file)
    print("Success")


if __name__ == "__main__":
    env_type = input("Enter environment (dev or prod): ")

    secret = get_secret(env_type)
    config = convert_to_dict(secret)
    env_file = os.path.dirname(os.path.realpath(__file__)) + "/../../.env"
    example_env_file = (
        os.path.dirname(os.path.realpath(__file__)) + "/../../.env.example"
    )
    write_to_env_file(config, env_file, example_env_file)

    env_appstore_file = (
        os.path.dirname(os.path.realpath(__file__)) + "/../../.env.appStore"
    )
    example_env_appstore_file = (
        os.path.dirname(os.path.realpath(__file__)) + "/../../.env.appStore.example"
    )
    write_to_env_appstore_file(env_appstore_file, example_env_appstore_file)
