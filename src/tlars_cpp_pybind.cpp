#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "carma_helper.h"
#include "tlars_cpp.h"

namespace py = pybind11;

PYBIND11_MODULE(tlars_cpp, m) {
    m.doc() = "Python bindings for the tlars C++ implementation";

    py::class_<tlars_cpp>(m, "tlars_cpp")
        // Constructors
        .def(py::init([](py::array_t<double> X, py::array_t<double> y, bool verbose, bool intercept, bool standardize, int num_dummies, std::string type) {
            return new tlars_cpp(carma::arr_to_mat(X), carma::arr_to_col(y), verbose, intercept, standardize, num_dummies, type);
        }), py::arg("X"), py::arg("y"), py::arg("verbose"), py::arg("intercept"), py::arg("standardize"), py::arg("num_dummies"), py::arg("type"))
        
        .def(py::init<py::dict>())

        // Methods
        .def("execute_lars_step", &tlars_cpp::execute_lars_step)

        // Output Getters
        .def("get_beta", &tlars_cpp::get_beta)
        .def("get_beta_path", &tlars_cpp::get_beta_path)
        .def("get_num_active", &tlars_cpp::get_num_active)
        .def("get_num_active_dummies", &tlars_cpp::get_num_active_dummies)
        .def("get_num_dummies", &tlars_cpp::get_num_dummies)
        .def("get_actions", &tlars_cpp::get_actions)
        .def("get_df", &tlars_cpp::get_df)
        .def("get_R2", &tlars_cpp::get_R2)
        .def("get_RSS", &tlars_cpp::get_RSS)
        .def("get_Cp", [](tlars_cpp& self) { return carma::col_to_arr(self.get_Cp()); })
        .def("get_lambda", [](tlars_cpp& self) { return carma::col_to_arr(self.get_lambda()); })
        .def("get_entry", &tlars_cpp::get_entry)
        .def("get_norm_X", [](tlars_cpp& self) { return carma::col_to_arr(self.get_norm_X()); })
        .def("get_mean_X", [](tlars_cpp& self) { return carma::col_to_arr(self.get_mean_X()); })
        .def("get_mean_y", &tlars_cpp::get_mean_y)
        .def("get_all", &tlars_cpp::get_all)

        // Properties
        .def_property("X", 
            [](tlars_cpp& self) { return carma::mat_to_arr(self.X); },
            [](tlars_cpp& self, py::array_t<double> X) { self.X = carma::arr_to_mat(X); }
        )
        .def_property("y",
            [](tlars_cpp& self) { return carma::col_to_arr(self.y); },
            [](tlars_cpp& self, py::array_t<double> y) { self.y = carma::arr_to_col(y); }
        )
        .def_readwrite("verbose", &tlars_cpp::verbose)
        .def_readwrite("intercept", &tlars_cpp::intercept)
        .def_readwrite("standardize", &tlars_cpp::standardize)
        .def_readwrite("num_dummies", &tlars_cpp::num_dummies)
        .def_readwrite("type", &tlars_cpp::type);
} 