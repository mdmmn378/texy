use serde_json::Value;
use std::collections::HashMap;

pub fn dedup_vector(arr: Vec<&str>) -> Vec<&str> {
    let mut v = arr.clone();
    v.sort_unstable();
    v.dedup();
    return v;
}

pub fn json_to_hashmap(json_string: &str) -> HashMap<String, Value> {
    serde_json::from_str(json_string).unwrap()
}

#[test]
fn test_dedup() {
    let input: Vec<&str> = vec!["a", "a", "b"];
    let output: Vec<&str> = vec!["a", "b"];
    assert_eq!(dedup_vector(input), output)
}

#[test]
fn test_json_to_hashmap() {
    let input = r#"{"key": 1}"#;
    println!("{:?}", json_to_hashmap(input));
}
