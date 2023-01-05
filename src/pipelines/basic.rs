use crate::components::actions::*;
use pyo3::prelude::*;
use rayon::prelude::*;

#[allow(unused_assignments)]
fn process_batch(items: Vec<String>) -> Vec<String> {
    let result = items
        .par_iter()
        .map(|elem| {
            let mut tmp = String::new();
            tmp = remove_newlines(elem.to_string());
            tmp = remove_urls(tmp);
            tmp = remove_emails(tmp);

            tmp = remove_infrequent_punctuations(tmp);
            tmp = merge_spaces(tmp);
            return tmp;
        })
        .collect();
    return result;
}

#[pyfunction]
#[allow(unused_assignments)]
pub fn run_basic(string_list: Vec<String>) -> PyResult<Vec<String>> {
    let result = process_batch(string_list);
    return Ok(result);
}

#[cfg(test)]
mod tests {

    use super::*;
    #[test]
    fn test_run_basic() -> PyResult<()> {
        Python::with_gil(|_py| {
            let res = run_basic(vec!["hello\t\n".to_string()]).unwrap();
            assert_eq!(res, vec!["hello".to_string()]);
            Ok(())
        })
    }
}
