pub mod components;
pub mod pipelines;
pub mod utils;
use pipelines::blocks::{extreme_clean, relaxed_clean, strict_clean};
use pyo3::prelude::*;

#[pymodule]
fn texy(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(strict_clean, m)?)?;
    m.add_function(wrap_pyfunction!(relaxed_clean, m)?)?;
    m.add_function(wrap_pyfunction!(extreme_clean, m)?)?;
    // let submodule = PyModule::new(_py, "components")?;
    // submodule.add_function(wrap_pyfunction!(merge_spaces, submodule)?)?; // functions must take
    // submodule.add_function(wrap_pyfunction!(remove_dot_commas, submodule)?)?;
    // m.add_submodule(submodule)?;
    Ok(())
}
