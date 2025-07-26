use crate::components::_emoticons::get_emoticons;
use regex::Regex;
use std::sync::OnceLock;

static EMAIL_REGEX: OnceLock<Regex> = OnceLock::new();
static URL_REGEX: OnceLock<Regex> = OnceLock::new();
static EMOJI_REGEX: OnceLock<Regex> = OnceLock::new();
static HTML_REGEX: OnceLock<Regex> = OnceLock::new();
static XML_REGEX: OnceLock<Regex> = OnceLock::new();

// Helper functions to get compiled regexes (compiled once, reused)
fn get_email_regex() -> &'static Regex {
    EMAIL_REGEX.get_or_init(|| Regex::new(r"[\w\.+-]+@[\w\.-]+\.[\w\.-]+").unwrap())
}

fn get_url_regex() -> &'static Regex {
    URL_REGEX.get_or_init(|| Regex::new(r#"http\S+"#).unwrap())
}

fn get_emoji_regex() -> &'static Regex {
    EMOJI_REGEX.get_or_init(|| {
        Regex::new(
            r#"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]"#
        ).unwrap()
    })
}

fn get_html_regex() -> &'static Regex {
    HTML_REGEX.get_or_init(|| Regex::new(r"<[^>]*>").unwrap())
}

fn get_xml_regex() -> &'static Regex {
    XML_REGEX.get_or_init(|| Regex::new(r"<[/]?[^>]+>").unwrap())
}

pub fn remove_newlines(string: String) -> String {
    // Safe replacement without unsafe code
    if !string.contains('\n') {
        return string;
    }
    string.replace('\n', " ")
}

pub fn remove_infrequent_punctuations(string: String) -> String {
    let delete_chars = r##""#$%&\'*+<=>@\\^_{|}~`"##;

    // Early return if no target characters
    let has_target_chars = string
        .chars()
        .any(|c| delete_chars.contains(c) || c == '\u{00a0}');
    if !has_target_chars {
        return string;
    }

    // Process characters efficiently
    let mut result = String::with_capacity(string.len());
    for c in string.chars() {
        if c == '\u{00a0}' {
            result.push(' ');
        } else if !delete_chars.contains(c) {
            result.push(c);
        }
        // Skip characters in delete_chars (effectively removing them)
    }

    result
}

pub fn remove_all_punctuations(mut string: String) -> String {
    let delete_chars = r##"!"#$%&\'()*+-/:;<=>?@[\\]^_{|}~`,.`"##;

    // Replace \xa0 first if present
    if string.contains('\u{00a0}') {
        string = string.replace('\u{00a0}', " ");
    }

    // Check if string contains any punctuation to avoid unnecessary processing
    let has_punctuation = string.chars().any(|c| delete_chars.contains(c));
    if !has_punctuation {
        return string;
    }

    // Safe character filtering and replacement
    string
        .chars()
        .map(|c| if delete_chars.contains(c) { ' ' } else { c })
        .collect()
}

pub fn remove_bn_numbers(string: String) -> String {
    // Bengali numbers: ০১২৩৪৫৬৭৮৯
    let bn_digits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];

    // Quick check if string contains any Bengali digits
    let has_bn_digits = string.chars().any(|c| bn_digits.contains(&c));
    if !has_bn_digits {
        return string;
    }

    // Filter out Bengali digits
    string
        .chars()
        .filter(|&c| !bn_digits.contains(&c))
        .collect()
}

pub fn unify_numbers(string: String) -> String {
    return string;
}

pub fn merge_spaces(string: String) -> String {
    if string.is_empty() {
        return string;
    }

    // Quick check if any space merging is needed
    let needs_processing = string.contains("  ")
        || string.contains('\t')
        || string.contains('\n')
        || string.contains('\r')
        || string.starts_with(' ')
        || string.ends_with(' ');

    if !needs_processing {
        return string;
    }

    // Efficient space merging using split_whitespace and join
    let words: Vec<&str> = string.split_whitespace().collect();
    if words.is_empty() {
        return String::new();
    }

    words.join(" ")
}

pub fn remove_emojis(string: String) -> String {
    // Check if string contains emojis first to avoid unnecessary processing
    if !string.chars().any(|c| c as u32 >= 0x1F300) {
        return string;
    }

    // Use direct string replacement to avoid regex overhead for small strings
    if string.len() < 100 {
        // For small strings, use simple character filtering
        string
            .chars()
            .filter(|&c| {
                let code = c as u32;
                !(code >= 0x1F300 && code <= 0x1F5FF)
                    && !(code >= 0x1F600 && code <= 0x1F64F)
                    && !(code >= 0x1F680 && code <= 0x1F6FF)
                    && !(code >= 0x1F700 && code <= 0x1F77F)
                    && !(code >= 0x1F780 && code <= 0x1F7FF)
                    && !(code >= 0x1F800 && code <= 0x1F8FF)
                    && !(code >= 0x1F900 && code <= 0x1F9FF)
                    && !(code >= 0x1FA00 && code <= 0x1FA6F)
                    && !(code >= 0x1FA70 && code <= 0x1FAFF)
                    && !(code >= 0x2702 && code <= 0x27B0)
            })
            .collect()
    } else {
        // For larger strings, use regex but avoid cloning
        get_emoji_regex().replace_all(&string, "").into_owned()
    }
}

pub fn remove_emoticons(string: String) -> String {
    // Quick length check - most emoticons are 2-3 characters
    if string.len() < 2 {
        return string;
    }

    // Quick scan to see if any emoticons might be present
    let has_common_chars = string.chars().any(|c| {
        matches!(
            c,
            ':' | ';' | '(' | ')' | '-' | '=' | 'D' | 'P' | 'X' | '^' | 'T' | '_' | '>' | '<'
        )
    });
    if !has_common_chars {
        return string; // No common emoticon characters found
    }

    // Store original length for comparison
    let original_len = string.len();
    let mut result = string;

    // Use a more efficient replacement strategy with a single pass
    let emoticons_to_replace = [
        // Most common emoticons
        ":)", ":(", ":D", ":P", ";)", ":-)", ":-(", ":-D", ":-P", ";-)", "=)", "=(", "=D", "=P",
        ":o", ":-o", ":O", ":-O", ":|", ":-|", // Additional common patterns
        "XD", "xD", ":x", ":X", "^^", "T_T", ">:(", "<3", ":3", ";P", ":S", ":s", ":'(", ":,(",
        ":-S", ":-s", "B)", "B-)", ":B", ":-B",
    ];

    // Process common emoticons with a single pass through the list
    for emo in &emoticons_to_replace {
        if result.contains(emo) {
            result = result.replace(emo, " ");
        }
    }

    // Only do additional processing if we have a moderate-sized string and found some emoticons
    if result.len() < original_len && result.len() > 50 && result.len() < 1000 {
        // Get full emoticons list for remaining processing, but limit scope
        let emoticons = get_emoticons();

        // Process a limited set of additional emoticons
        for emo in emoticons.iter().take(50) {
            if emo.len() > 1 && emo.len() <= 4 && result.contains(emo) {
                // Only process reasonable-length emoticons
                result = result.replace(emo, " ");
            }
        }
    }

    result
}

pub fn remove_urls(string: String) -> String {
    // Quick check to avoid regex if no URLs are present
    if !string.contains("http") {
        return string;
    }
    get_url_regex().replace_all(&string, "").into_owned()
}

pub fn remove_emails(string: String) -> String {
    // Quick check to avoid regex if no emails are present
    if !string.contains('@') {
        return string;
    }
    get_email_regex().replace_all(&string, "").into_owned()
}

pub fn remove_html(string: String) -> String {
    // Quick check to avoid regex if no HTML tags are present
    if !string.contains('<') {
        return string;
    }
    get_html_regex().replace_all(&string, "").into_owned()
}

pub fn remove_xml(string: String) -> String {
    // Quick check to avoid regex if no XML tags are present
    if !string.contains('<') {
        return string;
    }
    get_xml_regex().replace_all(&string, "").into_owned()
}
