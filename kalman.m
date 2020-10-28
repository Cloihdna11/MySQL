% Copyright 2009 - 2010 The MathWorks, Inc.
function [y ,err] = kalman(z) 
% Initialize state transition matrix

A=[ 1 z(1,2); 0 1];

% Measurement matrix
%H = [ 1 ];
H = [ 1 0];

Q = [1 0;
     0 3];

R = 10;


% Initial conditions
persistent x_est p_est
if isempty(x_est)
    x_est = zeros(2, 1);
    p_est = 5 * eye(2);
end

% Predicted state and covariance
x_prd = A * x_est;
p_prd = A * p_est * A' + Q;

% % Estimation
denom = H*p_prd*H';

klm_gain = p_prd * H' *inv(denom+R) ;


% Estimated state and covariance

x_est = x_prd + klm_gain * (z - H * x_prd);
p_est = p_prd - klm_gain * H * p_prd;

% Compute the estimated measurements
y = H * x_est;





