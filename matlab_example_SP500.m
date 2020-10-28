clc;
clear;
data = importdata('C:\Users\jdemp\VAR Heather Thesis\matlab\SP500_DP_dVIX_198602_2018121.csv');
%data = load('C:\Users\jdemp\Downloads\ssm-1.0.1\ssm-release\demos\data\seatbelt.dat');
% Load Data
% Data = readtable('Koopman UK Seatbelt dataset.xlsx');
%y = data(:,1);
%x = data(:,5); % alpha vector
 y = data.data(:,2);
 z = data.data(:,3); % alpha vector

% Setup a local level state space model
A = 1;
B = NaN;
C = 1;
D = NaN;
Mdl = ssm(A,B,C,D); % set up a local level SSM model
disp(Mdl);

% Estimate Parameters with exogenous variable
params0 = [0.1 0.1]; % initial values
[EstMdl, estParams] = estimate(Mdl, y(1:299), params0, 'Predictors', z(1:299), 'Univariate', 1);
varLevel = estParams(1)^2;
varObs = estParams(2)^2;
betaHat = estParams(3);
fprintf('varLevel = %5.4f, varObs = %5.4f, beta = %5.4f\n',varLevel,varObs,betaHat);
% Kalman filter/smoother
States = smooth(EstMdl,y(1:299),'Predictors',z(1:299),'Beta',betaHat);
yFit = States + betaHat*z(1:299);
irregular = y(1:299) - yFit; %Errors
mean((irregular(11:end,1)).^2)   % Mean Squared Error
RMSE = sqrt(mean((irregular(11:end)).^2));  % Root Mean Squared Error

% One-step-ahead forcast
clear irregular;

for i=300:length(y)
    [yFit,YMSE] = forecast(EstMdl,1,y(1:i-1),'Predictors0',z(1:i-1),'PredictorsF',z(i),'Beta',betaHat);
    irregular = y(i) - yFit; %Errors

end 
 
mean((irregular(11:end,1)).^2)   % Mean Squared Error
RMSE_out_of_sample = sqrt(mean((irregular).^2));  % Root Mean Squared Error

 
 
 
 
