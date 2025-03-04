#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "tlars_cpp.h"

namespace py = pybind11;

PYBIND11_MODULE(_tlars_cpp, m) {
    m.doc() = "Python bindings for TLARS C++ implementation";

    py::class_<TLARS>(m, "TLARS")
        .def(py::init<>())
        .def("fit", [](TLARS &self, py::array_t<double> X, py::array_t<double> y) {
            py::buffer_info X_buf = X.request();
            py::buffer_info y_buf = y.request();

            if (X_buf.ndim != 2)
                throw std::runtime_error("X must be a 2-D array");
            if (y_buf.ndim != 1)
                throw std::runtime_error("y must be a 1-D array");

            int n_samples = X_buf.shape[0];
            int n_features = X_buf.shape[1];

            if (y_buf.shape[0] != n_samples)
                throw std::runtime_error("X and y dimensions do not match");

            double* X_ptr = static_cast<double*>(X_buf.ptr);
            double* y_ptr = static_cast<double*>(y_buf.ptr);

            self.fit(X_ptr, y_ptr, n_samples, n_features);
        })
        .def("predict", [](TLARS &self, py::array_t<double> X) {
            py::buffer_info X_buf = X.request();

            if (X_buf.ndim != 2)
                throw std::runtime_error("X must be a 2-D array");

            int n_samples = X_buf.shape[0];
            int n_features = X_buf.shape[1];

            double* X_ptr = static_cast<double*>(X_buf.ptr);
            std::vector<double> predictions = self.predict(X_ptr, n_samples, n_features);

            return py::array_t<double>(predictions.size(), predictions.data());
        })
        .def("get_coefficients", &TLARS::get_coefficients)
        .def("get_intercept", &TLARS::get_intercept);
} 