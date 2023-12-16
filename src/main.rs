pub mod components;
pub mod pipelines;
pub mod utils;
use pipelines::blocks::{extreme, relaxed, strict};

fn leak() {
    let data = [
        "Hello, this is a sample text with\nnewlines.",
        "Visit https://example.com for more info!",
        "Send your feedback to feedback@example.com",
        "<p>This is an HTML paragraph.</p>",
        "<xml>This is some XML content.</xml>",
        "😃 Removing emoticons and emojis 😊 🚀",
        "This text has infrequent punctuations: !?#",
        "Multiple      spaces     between   words.",
    ];
    let mut v: Vec<String> = Vec::new();
    for _ in 0..100 {
        for i in &data {
            v.push(i.to_string());
        }
    }
    println!("Data size: {}", v.len());
    extreme(v.clone());
    relaxed(v.clone());
    strict(v.clone());
    println!("Done!");
}

fn main() {
    leak();
}
