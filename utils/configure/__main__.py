from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
import argparse
import json
from . import prompts


def run_prompt(prompt_class, default=None):
    styles = Style.from_dict({'prompt': 'bold',
                              'def': 'italic grey',
                              'rprompt': 'italic'})

    if default:
        prompt_class.default = default

    if hasattr(prompt_class, 'default'):
        text = [('class:prompt', '%s [' % prompt_class.prompt),
                ('class:def', prompt_class.default),
                ('class:prompt', ']: ')]

        default = prompt_class.default
    else:
        text = '{}: '.format(prompt_class.prompt)
        default = None

    result = prompt(text,
                    validator=prompt_class(),
                    validate_while_typing=False,
                    rprompt=prompt_class.help,
                    style=styles)

    if len(result) == 0 and default:
        result = default

    return result


def replace_cfnjson_value(data, key, value):
    for parameter in data:
        if parameter['ParameterKey'] == key:
            parameter['ParameterValue'] = value
            break

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', action='store', default='cloudformation/parameters.json')

    args = parser.parse_args()

    print('Prompting for Cloudformation parameters.')

    try:
        project_name = run_prompt(prompts.ProjectName)
        bucket_name = run_prompt(prompts.BucketName)
        environment_name = run_prompt(prompts.EnvironmentName)
        s3_key = run_prompt(prompts.S3Key, default='/lambda/%s.zip' % project_name.lower())
        python_runtime = run_prompt(prompts.PythonRuntime)
    except KeyboardInterrupt:
        return 1

    with open(args.config) as config_file:
        config = json.load(config_file)

    replace_cfnjson_value(config, 'ProjectName', project_name)
    replace_cfnjson_value(config, 'S3DeploymentBucketName', bucket_name)
    replace_cfnjson_value(config, 'EnvironmentName', environment_name)
    replace_cfnjson_value(config, 'S3DeploymentFileKey', s3_key)
    replace_cfnjson_value(config, 'Runtime', python_runtime)

    with open(args.config, 'w') as config_file:
        json.dump(config, config_file, indent=2)

    return 0


if __name__=='__main__':
    exit(main())
