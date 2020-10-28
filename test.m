%% Clear temporary variables
clear all;
load sp500.mat
numPts = 395;
err=zeros(numPts,1);
t=1:1:numPts;
% Kalman filter loop
for idx = 1: numPts
    % Get the input data
    z = sp500(idx,[2,4]);

    % Use Kalman filter to estimate the location
    [y,error] = kalman(z);
    
     err(idx,1) = error;
    
    % Plot the results

end

mean((err).^2)   % Mean Squared Error
RMSE = sqrt(mean((err).^2));  % Root Mean Squared Error

plot(t,err);

