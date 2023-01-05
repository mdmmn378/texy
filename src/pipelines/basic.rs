use crate::components::actions::*;
use pyo3::prelude::*;
use rayon::prelude::*;

#[allow(unused_assignments)]
fn schema_101(items: Vec<String>) -> Vec<String> {
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
            // tmp = remove_infrequent_punctuations(tmp);
            tmp = merge_spaces(tmp);
            return tmp;
        })
        .collect();
    return result;
}

#[pyfunction]
#[allow(unused_assignments)]
pub fn process_schema_101(string_list: Vec<String>) -> PyResult<Vec<String>> {
    let result = schema_101(string_list);
    return Ok(result);
}

#[cfg(test)]
mod tests {

    use super::*;
    #[test]
    fn test_run_basic() -> PyResult<()> {
        Python::with_gil(|_py| {
            let res = process_schema_101(vec!["hello\t\n".to_string()]).unwrap();
            assert_eq!(res, vec!["hello".to_string()]);
            Ok(())
        })
    }
}
