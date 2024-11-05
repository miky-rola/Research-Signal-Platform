from django.core.validators import RegexValidator


username_regex = r"^[a-zA-Z0-9_.-]+$"
email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
phone_number_regex = r"^\+?1?\d{9,15}$"


username_validator = RegexValidator(
    regex=username_regex,
    message="Username can only contain letters, numbers, dots, underscores, and hyphens.",
)

email_validator = RegexValidator(
    regex=email_regex, message="Enter a valid email address."
)

