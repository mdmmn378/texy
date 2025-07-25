use crate::components::actions::*;
use pyo3::prelude::*;
use rayon::prelude::*;

#[allow(unused_assignments)]
pub fn relaxed(items: Vec<String>) -> Vec<String> {
    items
        .into_par_iter()
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
    items
        .into_par_iter()
        .map(|elem| {
            let elem = remove_newlines(elem);
            let elem = remove_urls(elem);
            let elem = remove_emails(elem);
            let elem = remove_html(elem);
            let elem = remove_xml(elem);
            let elem = remove_emoticons(elem);
            let elem = remove_emojis(elem);
            let elem = remove_infrequent_punctuations(elem);
            merge_spaces(elem)
        })
        .collect()
}

#[allow(unused_assignments)]
pub fn extreme(items: Vec<String>) -> Vec<String> {
    items
        .into_par_iter()
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
pub fn relaxed_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    Ok(relaxed(string_list))
}

#[pyfunction]
pub fn strict_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    Ok(strict(string_list))
}

#[pyfunction]
pub fn extreme_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    Ok(extreme(string_list))
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
