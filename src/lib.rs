pub mod components;
pub mod pipelines;
pub mod utils;
use pipelines::basic::process_schema_101;
use pyo3::prelude::*;

#[pymodule]
fn _internal(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(process_schema_101, m)?)?;
    // let submodule = PyModule::new(_py, "components")?;
    // submodule.add_function(wrap_pyfunction!(run_basic, submodule)?)?;
    // m.add_submodule(submodule)?;
    Ok(())
}
