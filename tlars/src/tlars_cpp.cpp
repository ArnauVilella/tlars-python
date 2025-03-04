#include "tlars_cpp.h"
#include <stdexcept>
#include <algorithm>
#include <cmath>
#include <limits>

TLARS::TLARS() : intercept_(0.0), is_fitted_(false) {}

void TLARS::fit(double* X_ptr, double* y_ptr, int n_samples, int n_features) {
    // Convert input data to Eigen matrices
    Eigen::Map<Eigen::MatrixXd> X(X_ptr, n_samples, n_features);
    Eigen::Map<Eigen::VectorXd> y(y_ptr, n_samples);
    
    X_ = X;
    y_ = y;
    
    // Initialize coefficients
    coefficients_ = Eigen::VectorXd::Zero(n_features);
    
    // Standardize data
    standardize_data();
    
    // Compute LARS path
    compute_lars_path();
    
    is_fitted_ = true;
}

std::vector<double> TLARS::predict(double* X_ptr, int n_samples, int n_features) {
    if (!is_fitted_) {
        throw std::runtime_error("Model must be fitted before predicting");
    }
    
    if (n_features != coefficients_.size()) {
        throw std::runtime_error("Number of features in X does not match training data");
    }
    
    // Convert input data to Eigen matrix
    Eigen::Map<Eigen::MatrixXd> X(X_ptr, n_samples, n_features);
    
    // Make predictions
    Eigen::VectorXd predictions = X * coefficients_;
    predictions.array() += intercept_;
    
    // Convert to std::vector
    return std::vector<double>(predictions.data(), predictions.data() + predictions.size());
}

std::vector<double> TLARS::get_coefficients() const {
    if (!is_fitted_) {
        throw std::runtime_error("Model must be fitted before accessing coefficients");
    }
    return std::vector<double>(coefficients_.data(), coefficients_.data() + coefficients_.size());
}

double TLARS::get_intercept() const {
    if (!is_fitted_) {
        throw std::runtime_error("Model must be fitted before accessing intercept");
    }
    return intercept_;
}

void TLARS::standardize_data() {
    // Compute means
    Eigen::VectorXd X_mean = X_.colwise().mean();
    double y_mean = y_.mean();
    
    // Center X and y
    for (int i = 0; i < X_.rows(); ++i) {
        X_.row(i) -= X_mean.transpose();
    }
    y_.array() -= y_mean;
    
    // Scale X
    Eigen::VectorXd X_std = (X_.array().square().colwise().sum() / (X_.rows() - 1)).sqrt();
    for (int i = 0; i < X_.cols(); ++i) {
        X_.col(i) /= X_std(i);
    }
    
    // Store mean of y as intercept
    intercept_ = y_mean;
}

void TLARS::compute_lars_path() {
    int n = X_.rows();
    int p = X_.cols();
    
    // Initialize variables
    Eigen::VectorXd mu = Eigen::VectorXd::Zero(n);
    Eigen::VectorXd residuals = y_;
    std::vector<int> active_set;
    Eigen::VectorXd beta = Eigen::VectorXd::Zero(p);
    
    // Main LARS loop
    while (active_set.size() < std::min(n, p)) {
        // Compute correlations
        Eigen::VectorXd correlations = X_.transpose() * residuals;
        
        // Find maximum absolute correlation
        double max_corr = correlations.cwiseAbs().maxCoeff();
        
        // Add variable with maximum correlation to active set
        int j = 0;
        for (; j < p; ++j) {
            if (std::abs(correlations(j)) == max_corr && 
                std::find(active_set.begin(), active_set.end(), j) == active_set.end()) {
                break;
            }
        }
        active_set.push_back(j);
        
        // Extract active variables
        Eigen::MatrixXd X_active(n, active_set.size());
        for (size_t i = 0; i < active_set.size(); ++i) {
            X_active.col(i) = X_.col(active_set[i]);
        }
        
        // Compute direction using least squares
        Eigen::VectorXd direction = (X_active.transpose() * X_active)
                                      .ldlt()
                                      .solve(X_active.transpose() * residuals);
        
        // Update coefficients and residuals
        for (size_t i = 0; i < active_set.size(); ++i) {
            beta(active_set[i]) += direction(i);
        }
        
        mu = X_active * direction;
        residuals -= mu;
        
        // Check for convergence
        if (residuals.norm() < 1e-10) {
            break;
        }
    }
    
    // Store final coefficients
    coefficients_ = beta;
}

void TLARS::update_coefficients() {
    // This method can be used to update coefficients based on additional criteria
    // For now, we'll just keep the coefficients as they are
} 