from prompt_toolkit.validation import Validator, ValidationError


class ProjectName(Validator):
    prompt = 'Project Name'

    def validate(self, document):
        text = document.text

        if len(text) > 92:
            raise ValidationError(message='The Project Name must be 92 characters or less.')

        if len(text) > 0 and not text[0].isalpha():
            raise ValidationError(message='The Project Name must start with a letter.')

        if len(text) < 3:
            raise ValidationError(message='Must be at least 3 characters.')

    @staticmethod
    def help():
        return 'Give your project a unique name.'


class BucketName(Validator):
    prompt = 'S3 Bucket Name'

    def validate(self, document):
        text = document.text

        if text.lower() != text:
            raise ValidationError(message='Bucket Names must be lower case.')

        if '_' in text:
            raise ValidationError(message='Bucket Names cannot contain underscores.')

        if len(text) < 3:
            raise ValidationError(message='Must be at least 3 characters.')

    @staticmethod
    def help():
        return 'An S3 bucket for Lambda deployments, does not need to be unique.'


class EnvironmentName(Validator):
    prompt = 'Environment Name'

    default = 'dev'

    def validate(self, document):
        text = document.text

        if text.lower() != text:
            raise ValidationError(message='Environment Names should be lower case.')

    @staticmethod
    def help():
        return 'A name for this Lambda environment (dev, prod, etc).'


class S3Key(Validator):
    prompt = 'Lambda S3 Key'

    def validate(self, document):
        text = document.text

    @staticmethod
    def help():
        return 'The S3 key (filename) for the Lambda zip file.'


class PythonRuntime(Validator):
    prompt = 'Python Runtime'

    default = 'python3.6'

    choices = ('python2.7', 'python3.6',)

    def validate(self, document):
        text = document.text

        if len(text) > 0 and text not in self.choices:
            raise ValidationError(message='Must be one of: {}'.format(self.choices))

    @staticmethod
    def help():
        return 'The version of Python to use (python2.7 or python3.6)'
