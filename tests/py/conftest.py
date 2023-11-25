import pytest


@pytest.fixture(scope="session")
def sample_input():
    return [
        "Hello, this is a sample text with\nnewlines.",
        "Visit https://example.com for more info!",
        "Send your feedback to feedback@example.com",
        "<p>This is an HTML paragraph.</p>",
        "<xml>This is some XML content.</xml>",
        "😃 Removing emoticons and emojis 😊 🚀",
        "This text has infrequent punctuations: !?#",
        "Multiple      spaces     between   words.",
    ]


@pytest.fixture(scope="session")
def strict_output():
    return [
        "Hello, this is a sample text with newlines.",
        "Visit for more info!",
        "Send your feedback to",
        "This is an HTML paragraph.",
        "This is some XML content.",
        "Removing emoticons and emojis",
        "This text has infrequent punctuations: !?",
        "Multiple spaces between words.",
    ]


@pytest.fixture(scope="session")
def relaxed_output():
    return [
        "Hello, this is a sample text with newlines.",
        "Visit https://example.com for more info!",
        "Send your feedback to feedback@example.com",
        "This is an HTML paragraph.",
        "This is some XML content.",
        "😃 Removing emoticons and emojis 😊 🚀",
        "This text has infrequent punctuations: !?#",
        "Multiple spaces between words.",
    ]


@pytest.fixture(scope="session")
def extreme_output():
    return [
        "Hello this is a sample text with newlines",
        "Visit for more info",
        "Send your feedback to",
        "This is an HTML paragraph",
        "This is some XML content",
        "Removing emoticons and emojis",
        "This text has infrequent punctuations",
        "Multiple spaces between words",
    ]
