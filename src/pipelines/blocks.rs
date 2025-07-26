use crate::components::actions::*;
use pyo3::prelude::*;

#[allow(unused_assignments)]
pub fn relaxed(items: Vec<String>) -> Vec<String> {
    // Pre-allocate result vector with exact capacity to avoid reallocations
    let mut result = Vec::with_capacity(items.len());

    // Process items individually to minimize peak memory usage
    for item in items {
        let processed = {
            let item = remove_newlines(item);
            let item = remove_html(item);
            let item = remove_xml(item);
            merge_spaces(item)
        };
        result.push(processed);
    }

    // Shrink vector to exact size to free unused capacity
    result.shrink_to_fit();
    result
}

#[allow(unused_assignments)]
pub fn strict(items: Vec<String>) -> Vec<String> {
    // Pre-allocate result vector with exact capacity
    let mut result = Vec::with_capacity(items.len());

    // Process items individually for better memory control
    for item in items {
        let processed = {
            let item = remove_newlines(item);
            let item = remove_urls(item);
            let item = remove_emails(item);
            let item = remove_html(item);
            let item = remove_xml(item);
            let item = remove_emoticons(item);
            let item = remove_emojis(item);
            let item = remove_infrequent_punctuations(item);
            merge_spaces(item)
        };
        result.push(processed);
    }

    // Shrink vector to exact size
    result.shrink_to_fit();
    result
}

#[allow(unused_assignments)]
pub fn extreme(items: Vec<String>) -> Vec<String> {
    // Pre-allocate result vector with exact capacity
    let mut result = Vec::with_capacity(items.len());

    // Process items individually for optimal memory control
    for item in items {
        let processed = {
            let item = remove_newlines(item);
            let item = remove_urls(item);
            let item = remove_emails(item);
            let item = remove_html(item);
            let item = remove_xml(item);
            let item = remove_emoticons(item);
            let item = remove_emojis(item);
            let item = remove_all_punctuations(item);
            merge_spaces(item)
        };
        result.push(processed);
    }

    // Shrink vector to exact size
    result.shrink_to_fit();
    result
}

#[pyfunction]
pub fn relaxed_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    // Process directly without unnecessary Python GIL operations
    let result = relaxed(string_list);
    Ok(result)
}

#[pyfunction]
pub fn strict_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    // Process directly without unnecessary Python GIL operations
    let result = strict(string_list);
    Ok(result)
}

#[pyfunction]
pub fn extreme_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    // Process directly without unnecessary Python GIL operations
    let result = extreme(string_list);
    Ok(result)
}

// #[cfg(test)]
// mod tests {

//     use super::*;
//     #[test]
//     fn test_py_strict() -> PyResult<()> {
//         Python::with_gil(|_py| {
//             let res = strict_clean(vec!["hello\t\n".to_string()]).unwrap();
//             assert_eq!(res, vec!["hello".to_string()]);
//             Ok(())
//         })
//     }

//     #[test]
//     fn test_py_relaxed() -> PyResult<()> {
//         Python::with_gil(|_py| {
//             let res = relaxed_clean(vec!["hello\t\n".to_string()]).unwrap();
//             assert_eq!(res, vec!["hello".to_string()]);
//             Ok(())
//         })
//     }

//     #[test]
//     fn test_py_extreme() -> PyResult<()> {
//         Python::with_gil(|_py| {
//             let res = extreme_clean(vec!["hello\t\n".to_string()]).unwrap();
//             assert_eq!(res, vec!["hello".to_string()]);
//             Ok(())
//         })
//     }
// }
