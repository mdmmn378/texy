use crate::components::_emoticons::get_emoticons;
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    pub static ref RE_EMAIL: Regex = Regex::new(r"[\w\.+-]+@[\w\.-]+\.[\w\.-]+").unwrap();
    pub static ref RE_URL: Regex = Regex::new(r#"http\S+"#).unwrap();
    pub static ref RE_EMOJI: Regex = Regex::new(
        r#"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]"#
    )
    .unwrap();
    pub static ref RE_HTML: Regex = Regex::new(r"<[^>]*>").unwrap();
    pub static ref RE_XML: Regex = Regex::new(r"<[/]?[^>]+>").unwrap();
}

pub fn remove_newlines(mut string: String) -> String {
    // In-place replacement to avoid allocations
    unsafe {
        let bytes = string.as_mut_vec();
        for byte in bytes.iter_mut() {
            if *byte == b'\n' {
                *byte = b' ';
            }
        }
    }
    string
}

pub fn remove_infrequent_punctuations(mut string: String) -> String {
    let delete_chars = r##""#$%&\'*+<=>@\\^_{|}~`"##;

    // Replace \xa0 first
    if string.contains('\u{00a0}') {
        string = string.replace('\u{00a0}', " ");
    }

    // Filter characters in place to avoid allocations
    string.retain(|c| !delete_chars.contains(c));
    string
}

pub fn remove_all_punctuations(mut string: String) -> String {
    let delete_chars = r##"!"#$%&\'()*+-/:;<=>?@[\\]^_{|}~`"##;

    // Replace \xa0 first
    if string.contains('\u{00a0}') {
        string = string.replace('\u{00a0}', " ");
    }

    // Filter and replace in a single pass to minimize allocations
    string.retain(|c| !delete_chars.contains(c) && c != ',' && c != '.');

    // Replace remaining commas and periods with spaces in-place
    unsafe {
        let bytes = string.as_mut_vec();
        for byte in bytes.iter_mut() {
            if *byte == b',' || *byte == b'.' {
                *byte = b' ';
            }
        }
    }
    string
}

pub fn remove_bn_numbers(mut string: String) -> String {
    let bn_nums = "০১৭২১৭৬৯৫৫০";
    string.retain(|c| !bn_nums.contains(c));
    string
}

pub fn unify_numbers(string: String) -> String {
    return string;
}

pub fn merge_spaces(string: String) -> String {
    // More efficient space merging without allocating intermediate vectors
    let mut result = String::with_capacity(string.len());
    let mut chars = string.chars();
    let mut prev_was_space = false;

    while let Some(ch) = chars.next() {
        if ch.is_whitespace() {
            if !prev_was_space {
                result.push(' ');
                prev_was_space = true;
            }
        } else {
            result.push(ch);
            prev_was_space = false;
        }
    }

    result.trim().to_string()
}

pub fn remove_emojis(string: String) -> String {
    // Use into_owned to avoid unnecessary cloning
    RE_EMOJI.replace_all(&string, "").into_owned()
}

pub fn remove_emoticons(mut string: String) -> String {
    // Optimize emoticon removal to minimize allocations
    for emo in get_emoticons().iter() {
        if string.contains(emo) {
            // Use efficient replacement
            string = string.replace(emo, " ");
        }
    }
    string
}

pub fn remove_urls(string: String) -> String {
    RE_URL.replace_all(&string, "").to_string()
}

pub fn remove_emails(string: String) -> String {
    RE_EMAIL.replace_all(&string, "").to_string()
}

pub fn remove_html(string: String) -> String {
    RE_HTML.replace_all(&string, "").to_string()
}

pub fn remove_xml(string: String) -> String {
    RE_XML.replace_all(&string, "").to_string()
}
