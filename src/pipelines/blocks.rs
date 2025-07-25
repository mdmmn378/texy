use crate::components::actions::*;
use pyo3::prelude::*;

#[allow(unused_assignments)]
pub fn relaxed(items: Vec<String>) -> Vec<String> {
    // Use sequential processing to avoid rayon thread pool memory retention
    items
        .into_iter()
        .map(|elem| {
            let elem = remove_newlines(elem);
            let elem = remove_html(elem);
            let elem = remove_xml(elem);
            merge_spaces(elem)
        })
        .collect()
}

#[allow(unused_assignments)]
pub fn strict(items: Vec<String>) -> Vec<String> {
    // Simplified strict processing to identify leak source
    items
        .into_iter()
        .map(|mut elem| {
            // Test with minimal operations
            elem = remove_newlines(elem);
            elem = remove_urls(elem);
            elem = remove_emails(elem);
            // Skip potentially problematic operations
            // elem = remove_html(elem);
            // elem = remove_xml(elem);
            // elem = remove_emojis(elem);
            // elem = remove_infrequent_punctuations(elem);
            merge_spaces(elem)
        })
        .collect()
}

#[allow(unused_assignments)]
pub fn extreme(items: Vec<String>) -> Vec<String> {
    // Use sequential processing to avoid rayon thread pool memory retention
    items
        .into_iter()
        .map(|elem| {
            let elem = remove_newlines(elem);
            let elem = remove_urls(elem);
            let elem = remove_emails(elem);
            let elem = remove_html(elem);
            let elem = remove_xml(elem);
            let elem = remove_emoticons(elem);
            let elem = remove_emojis(elem);
            let elem = remove_all_punctuations(elem);
            merge_spaces(elem)
        })
        .collect()
}

#[pyfunction]
pub fn relaxed_clean(py: Python<'_>, string_list: Vec<String>) -> PyResult<Vec<String>> {
    // Ultra-aggressive memory management for PyO3
    let result = py.allow_threads(|| {
        // Process without intermediate cloning
        relaxed(string_list)
    });

    // Multiple garbage collection calls
    py.run("import gc; [gc.collect() for _ in range(3)]", None, None)?;

    Ok(result)
}

#[pyfunction]
pub fn strict_clean(py: Python<'_>, string_list: Vec<String>) -> PyResult<Vec<String>> {
    // Ultra-aggressive memory management for PyO3
    let result = py.allow_threads(|| {
        // Process without intermediate cloning
        strict(string_list)
    });

    // Multiple garbage collection calls
    py.run("import gc; [gc.collect() for _ in range(3)]", None, None)?;

    Ok(result)
}

#[pyfunction]
pub fn extreme_clean(py: Python<'_>, string_list: Vec<String>) -> PyResult<Vec<String>> {
    // Ultra-aggressive memory management for PyO3
    let result = py.allow_threads(|| {
        // Process without intermediate cloning
        extreme(string_list)
    });

    // Multiple garbage collection calls
    py.run("import gc; [gc.collect() for _ in range(3)]", None, None)?;
    py.run("import gc; gc.collect()", None, None)?;

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
