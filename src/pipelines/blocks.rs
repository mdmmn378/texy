use crate::components::actions::*;
use pyo3::prelude::*;
use rayon::prelude::*;

#[allow(unused_assignments)]
pub fn relaxed(items: Vec<String>) -> Vec<String> {
    let result = items
        .par_iter()
        .map(|elem| {
            let mut tmp = String::new();
            tmp = remove_newlines(elem.to_string());
            tmp = remove_html(tmp);
            tmp = remove_xml(tmp);
            tmp = merge_spaces(tmp);
            return tmp;
        })
        .collect();
    return result;
}

#[allow(unused_assignments)]
pub fn strict(items: Vec<String>) -> Vec<String> {
    let result = items
        .par_iter()
        .map(|elem| {
            let mut tmp = String::new();
            tmp = remove_newlines(elem.to_string());
            tmp = remove_urls(tmp);
            tmp = remove_emails(tmp);
            tmp = remove_html(tmp);
            tmp = remove_xml(tmp);
            tmp = remove_emoticons(tmp);
            tmp = remove_emojis(tmp);
            tmp = remove_infrequent_punctuations(tmp);
            tmp = merge_spaces(tmp);
            return tmp;
        })
        .collect();
    return result;
}

#[allow(unused_assignments)]
pub fn extreme(items: Vec<String>) -> Vec<String> {
    let result = items
        .par_iter()
        .map(|elem| {
            let mut tmp = String::new();
            tmp = remove_newlines(elem.to_string());
            tmp = remove_urls(tmp);
            tmp = remove_emails(tmp);
            tmp = remove_html(tmp);
            tmp = remove_xml(tmp);
            tmp = remove_emoticons(tmp);
            tmp = remove_emojis(tmp);
            tmp = remove_all_punctuations(tmp);
            tmp = merge_spaces(tmp);
            return tmp;
        })
        .collect();
    return result;
}

#[pyfunction]
#[allow(unused_assignments)]
pub fn relaxed_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    let result = relaxed(string_list);
    return Ok(result);
}

#[pyfunction]
#[allow(unused_assignments)]
pub fn strict_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    let result = strict(string_list);
    return Ok(result);
}

#[pyfunction]
#[allow(unused_assignments)]
pub fn extreme_clean(string_list: Vec<String>) -> PyResult<Vec<String>> {
    let result = extreme(string_list);
    return Ok(result);
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
