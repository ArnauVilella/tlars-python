#ifndef tlars_cpp_H
#define tlars_cpp_H

#include <vector>
#include <list>
#include <string>
#include <Eigen/Dense>

class TLARS {
public:
    // Constructors
    TLARS();
    
    // Methods
    void fit(double* X_ptr, double* y_ptr, int n_samples, int n_features);
    std::vector<double> predict(double* X_ptr, int n_samples, int n_features);
    std::vector<double> get_coefficients() const;
    double get_intercept() const;

private:
    // Internal state
    Eigen::MatrixXd X_;
    Eigen::VectorXd y_;
    Eigen::VectorXd coefficients_;
    double intercept_;
    bool is_fitted_;
    
    // Helper methods
    void standardize_data();
    void compute_lars_path();
    void update_coefficients();
};

#endif /* tlars_cpp_H */ 