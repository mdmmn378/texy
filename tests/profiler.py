import copy
import gc

from memory_profiler import profile


def dummy_clean(data):
    return copy.deepcopy(data)


@profile
def profile_extreme_clean():
    print("Profiling extreme_clean")
    from texy.pipelines import extreme_clean

    data = [
        "Hello, this is a sample text with\nnewlines.",
        "Visit https://example.com for more info!",
        "Send your feedback to feedback@example.com",
        "<p>This is an HTML paragraph.</p>",
        "<xml>This is some XML content.</xml>",
        "😃 Removing emoticons and emojis 😊 🚀",
        "This text has infrequent punctuations: !?#",
        "Multiple      spaces     between   words.",
    ] * 100000
    cleaned_data = extreme_clean(data)

    del cleaned_data
    del data
    gc.collect()
    ...


@profile
def profile_dummy_clean():
    data = [
        "Hello, this is a sample text with\nnewlines.",
        "Visit https://example.com for more info!",
        "Send your feedback to feedback@example.com",
        "<p>This is an HTML paragraph.</p>",
        "<xml>This is some XML content.</xml>",
        "😃 Removing emoticons and emojis 😊 🚀",
        "This text has infrequent punctuations: !?#",
        "Multiple      spaces     between   words.",
    ] * 100000

    cleaned_data = dummy_clean(data)
    gc.collect()
    del cleaned_data
    del data


if __name__ == "__main__":
    profile_extreme_clean()
    # profile_extreme_clean()
    # profile_dummy_clean()
