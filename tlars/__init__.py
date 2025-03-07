from .tlars_cpp import tlars_cpp
import numpy as np
import time
import matplotlib.pyplot as plt
from typing import Optional, List, Dict, Union, Any, Tuple

class TLARS:
    """
    Python wrapper for the Terminating-LARS (T-LARS) algorithm.
    
    Parameters
    ----------
    X : numpy.ndarray
        Real valued predictor matrix.
    y : numpy.ndarray
        Response vector.
    verbose : bool, default=False
        If True, progress in computations is shown.
    intercept : bool, default=True
        If True, an intercept is included.
    standardize : bool, default=True
        If True, the predictors are standardized and the response is centered.
    num_dummies : int, default=0
        Number of dummies that are appended to the predictor matrix.
    type : str, default='lar'
        Type of used algorithm (currently possible choices: 'lar' or 'lasso').
    lars_state : dict, optional
        Dictionary of variables associated with previous T-LARS step (necessary to restart
        the forward selection process exactly where it was previously terminated). The lars_state
        is extracted from a TLARS object via get_all() and is only required when the
        object is deleted or got lost in another Python session.
    info : bool, default=True
        If True and object is not recreated from previous T-LARS state, then information about 
        the created object is printed.
    """
    
    def __init__(self, X=None, y=None, verbose=False, intercept=True, standardize=True, 
                 num_dummies=0, type='lar', lars_state=None, info=True):
        # If a previous state is provided, use it to initialize
        if lars_state is not None:
            if not isinstance(lars_state, dict) or len(lars_state) != 4:
                raise ValueError("'lars_state' must be a dictionary containing the state variables "
                               "of a TLARS object. It must be obtained via model.get_all().")
            self._model = tlars_cpp(lars_state)
        else:
            # Input validation
            if X is None or y is None:
                raise ValueError("X and y must be provided when not initializing from lars_state")
                
            if not isinstance(X, np.ndarray):
                raise ValueError("'X' must be a numpy array.")
                
            if not isinstance(y, (np.ndarray, list)):
                raise ValueError("'y' must be a numpy array or list.")
                
            if np.isnan(X).any():
                raise ValueError("'X' contains NaN values. Please remove or impute them before proceeding.")
                
            if np.isnan(y).any():
                raise ValueError("'y' contains NaN values. Please remove or impute them before proceeding.")
                
            # Convert inputs to numpy arrays if they aren't already
            X = np.asarray(X, dtype=np.float64)
            y = np.asarray(y, dtype=np.float64)
            
            # Ensure y is a vector
            if y.ndim > 1:
                y = y.flatten()
                
            if X.shape[0] != len(y):
                raise ValueError("Number of rows in X does not match length of y.")
                
            if not isinstance(num_dummies, int) or num_dummies < 0 or num_dummies > X.shape[1]:
                raise ValueError("'num_dummies' must be an integer >= 0 and <= the number of columns in X.")
                
            if not standardize:
                import warnings
                warnings.warn("'standardize' should be True for the T-LARS algorithm. "
                            "Since you set standardize=False, we hope you have a good reason for doing that!")
                
            if type not in ['lar', 'lasso']:
                raise ValueError("'type' must be one of 'lar', 'lasso'.")
            
            # Create the C++ object
            self._model = tlars_cpp(X, y, verbose, intercept, standardize, num_dummies, type)
            
            # Print information if requested
            if info:
                print(f"Created a TLARS object...")
                print(f"\t\t The first p = {X.shape[1] - num_dummies} predictors are the original predictors and")
                print(f"\t\t the last num_dummies = {num_dummies} predictors are dummies")
    
    def fit(self, T_stop=None, early_stop=True, info=True):
        """
        Fit the TLARS model.
        
        Parameters
        ----------
        T_stop : int, optional
            Number of included dummies after which the random experiments 
            (i.e., forward selection processes) are stopped.
        early_stop : bool, default=True
            If True, then the forward selection process is stopped after T_stop 
            dummies have been included. Otherwise the entire solution path is computed.
        info : bool, default=True
            If True, information about the T-LARS step is printed.
            
        Returns
        -------
        self : object
            Returns self.
        """
        # Set default T_stop to number of dummies if not provided
        if T_stop is None:
            T_stop = self._model.num_dummies
        
        # Validate T_stop
        num_dummies = self._model.num_dummies
        if not (1 <= T_stop <= num_dummies):
            raise ValueError(f"Value of 'T_stop' not valid. 'T_stop' must be an integer from 1 to {num_dummies}.")
            
        if not early_stop:
            print("'T_stop' is ignored. Computing the entire solution path...")
            
        # Execute T-LARS step and print information if info=True
        if info:
            print("Executing T-LARS step by reference...")
            
            # Execute and time T-LARS step
            start_time = time.time()
            self._model.execute_lars_step(T_stop, early_stop)
            elapsed = time.time() - start_time
            
            # Print information about the executed T-LARS step
            if early_stop:
                print(f"\t\t Finished T-LARS step(s)...")
                print(f"\t\t\t - The results are stored in the TLARS object.")
                print(f"\t\t\t - New value of T_stop: {T_stop}.")
                print(f"\t\t\t - Time elapsed: {elapsed:.3f} sec.")
            else:
                print(f"\t\t Finished T-LARS step(s). No early stopping!")
                print(f"\t\t\t - The results are stored in the TLARS object.")
                print(f"\t\t\t - Time elapsed: {elapsed:.3f} sec.")
        else:
            # Execute T-LARS step without info
            self._model.execute_lars_step(T_stop, early_stop)
            
        return self
    
    def plot(self, xlabel="# Included dummies", ylabel="Coefficients", 
             include_dummies=True, show_actions=True, 
             col_selected="black", col_dummies="red",
             ls_selected="-", ls_dummies="--",
             legend_pos="best", figsize=(10, 6)):
        """
        Plot the T-LARS solution path.
        
        Parameters
        ----------
        xlabel : str, default="# Included dummies"
            Label for the x-axis.
        ylabel : str, default="Coefficients"
            Label for the y-axis.
        include_dummies : bool, default=True
            If True, solution paths of dummies are added to the plot.
        show_actions : bool, default=True
            If True, marks for added variables are shown above the plot.
        col_selected : str, default="black"
            Color of lines corresponding to selected variables.
        col_dummies : str, default="red"
            Color of lines corresponding to included dummies.
        ls_selected : str, default="-"
            Line style of lines corresponding to selected variables.
        ls_dummies : str, default="--"
            Line style of lines corresponding to included dummies.
        legend_pos : str, default="best"
            Legend position.
        figsize : tuple, default=(10, 6)
            Figure size.
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            The matplotlib figure object.
        ax : matplotlib.axes.Axes
            The matplotlib axes object.
        """
        # Check if the type is 'lar'
        method_type = self._model.type
        if method_type != "lar":
            raise ValueError("Plot is only generated for LARS, not Lasso! Set type='lar' when creating a TLARS object.")
        
        # Retrieve data to be plotted
        T_stop = self._model.get_num_active_dummies()
        num_dummies = self._model.get_num_dummies()
        var_select_path = self._model.get_actions()
        beta_path = np.array(self._model.get_beta_path())
        
        # Number of original variables (without dummies)
        p = beta_path.shape[1] - num_dummies
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        # Generate solution path plot of active variables
        dummies_path = [i+1 for i, v in enumerate(var_select_path) if v > p]
        dummies_path_labels = range(1, T_stop+1)
        
        # Plot original variables
        for i in range(p):
            ax.plot(beta_path[:, i], color=col_selected, linestyle=ls_selected)
        
        # Set x-axis ticks to match included dummies
        ax.set_xticks(dummies_path)
        ax.set_xticklabels(dummies_path_labels)
        
        # Add vertical lines for included dummies
        for dummy_pos in dummies_path:
            ax.axvline(x=dummy_pos, color=col_dummies, linestyle='-', linewidth=1.3, alpha=0.5)
        
        # Add dummies solution path to plot
        if include_dummies:
            for i in range(p, p + num_dummies):
                ax.plot(beta_path[:, i], color=col_dummies, linestyle=ls_dummies)
        
        # Add markers for actions
        if show_actions:
            ax2 = ax.twiny()
            
            # Get positions of actions
            var_select_path_positions = range(1, len(var_select_path) + 1)
            
            # Convert dummy indices to 'D'
            var_select_path_labels = []
            for v in var_select_path:
                if v > p:
                    var_select_path_labels.append('D')
                else:
                    var_select_path_labels.append(str(v))
            
            # Set ticks for action markers
            ax2.set_xticks(var_select_path_positions)
            ax2.set_xticklabels(var_select_path_labels)
            ax2.set_xlabel("Index of selected variables (D indicates an included dummy)")
            
            # Add vertical lines for actions
            for action_pos in var_select_path_positions:
                ax.axvline(x=action_pos, color='gray', linestyle=':', alpha=0.5)
        
        # Add legend if showing both variable types
        if include_dummies:
            ax.legend(['Original variables', 'Dummies'], loc=legend_pos)
        
        # Set labels
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Adjust layout
        plt.tight_layout()
        
        return fig, ax
    
    def get_all(self):
        """
        Get all state variables of the model.
        
        Returns
        -------
        dict
            Dictionary containing all state variables.
        """
        return self._model.get_all()
    
    @property
    def coef_(self):
        """
        Get the coefficients of the model.
        
        Returns
        -------
        numpy.ndarray
            The coefficients of the model.
        """
        return np.array(self._model.get_beta())
    
    @property
    def coef_path_(self):
        """
        Get the coefficient path.
        
        Returns
        -------
        list
            A list of coefficient vectors at each step.
        """
        return self._model.get_beta_path()
    
    @property
    def n_active_(self):
        """
        Get the number of active predictors.
        
        Returns
        -------
        int
            The number of active predictors.
        """
        return self._model.get_num_active()
    
    @property
    def n_active_dummies_(self):
        """
        Get the number of active dummy variables.
        
        Returns
        -------
        int
            The number of active dummy variables.
        """
        return self._model.get_num_active_dummies()
    
    @property
    def n_dummies_(self):
        """
        Get the total number of dummy variables.
        
        Returns
        -------
        int
            The total number of dummy variables.
        """
        return self._model.get_num_dummies()
    
    @property
    def actions_(self):
        """
        Get the indices of added/removed variables along the solution path.
        
        Returns
        -------
        list
            The indices of added/removed variables.
        """
        return self._model.get_actions()
    
    @property
    def df_(self):
        """
        Get the degrees of freedom at each step.
        
        Returns
        -------
        list
            The degrees of freedom at each step.
        """
        return self._model.get_df()
    
    @property
    def r2_(self):
        """
        Get the R^2 statistic at each step.
        
        Returns
        -------
        list
            The R^2 statistic at each step.
        """
        return self._model.get_R2()
    
    @property
    def rss_(self):
        """
        Get the residual sum of squares at each step.
        
        Returns
        -------
        list
            The residual sum of squares at each step.
        """
        return self._model.get_RSS()
    
    @property
    def cp_(self):
        """
        Get the Cp-statistic at each step.
        
        Returns
        -------
        numpy.ndarray
            The Cp-statistic at each step.
        """
        return self._model.get_Cp()
    
    @property
    def lambda_(self):
        """
        Get the lambda-values (penalty parameters) at each step.
        
        Returns
        -------
        numpy.ndarray
            The lambda-values at each step.
        """
        return self._model.get_lambda()
    
    @property
    def entry_(self):
        """
        Get the first entry/selection steps of the predictors.
        
        Returns
        -------
        list
            The first entry/selection steps of the predictors.
        """
        return self._model.get_entry()
    
    def __repr__(self):
        """
        Get a string representation of the model.
        
        Returns
        -------
        str
            A string representation of the model.
        """
        p = len(self.coef_) - self.n_dummies_
        selected_vars = [v for v in self.actions_ if v <= p]
        
        if len(selected_vars) == 0:
            selected_var_str = "No variables selected"
        else:
            selected_var_str = ", ".join(map(str, selected_vars))
            
        return (f"TLARS object:\n"
                f"\t - Number of dummies: {self.n_dummies_}\n"
                f"\t - Number of included dummies: {self.n_active_dummies_}\n"
                f"\t - Selected variables: {selected_var_str}")

# Generate Gaussian data similar to the R package example
def generate_gaussian_data(n=50, p=100, seed=789):
    """
    Generate toy data from a Gaussian linear model.
    
    Parameters
    ----------
    n : int, default=50
        Number of observations.
    p : int, default=100
        Number of variables.
    seed : int, default=789
        Random seed for reproducibility.
        
    Returns
    -------
    dict
        Dictionary containing X, y, beta, and support.
    """
    np.random.seed(seed)
    X = np.random.randn(n, p)
    beta = np.zeros(p)
    beta[:3] = 5
    support = beta > 0
    y = X @ beta + np.random.randn(n)
    
    return {
        'X': X,
        'y': y,
        'beta': beta,
        'support': support
    }

# Create a named dataset similar to the R package
gaussian_data = generate_gaussian_data()
