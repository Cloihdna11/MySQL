clc;
clear;
% data = importdata('C:\Users\jdemp\VAR Heather Thesis\matlab\SP500_DP_dVIX_198602_2018121.csv');
data = load('C:\Users\jdemp\Downloads\ssm-1.0.1\ssm-release\demos\data\seatbelt.dat');

y = data(:,1);
z = data(:,5);
% Setup a local level state space model
A = 1;
B = NaN;
C = 1;
D = NaN;
Mdl = ssm(A,B,C,D); % set up a local level SSM model
disp(Mdl);


% Estimate Parameters with exogenous variable
params0 = [0.1 0.1]; % initial values
[EstMdl, estParams] = estimate(Mdl, y, params0, 'Predictors', z, 'Univariate', 1);
varLevel = estParams(1)^2;
varObs = estParams(2)^2;
betaHat = estParams(3);
fprintf('varLevel = %5.4f, varObs = %5.4f, beta = %5.4f\n',varLevel,varObs,betaHat);
% Kalman filter/smoother
States = smooth(EstMdl,y,'Predictors',z,'Beta',betaHat);
yFit = States + betaHat*z;
irregular = y - yFit; %Errors
mean((irregular(11:end)).^2)   % Mean Squared Error
RMSE = sqrt(mean((irregular(11:end)).^2));  % Root Mean Squared Error

% One-step-ahead forcast
yF = forecast(EstMdl,1,y(1:end-1),'Predictors0',z(1:end-1),'PredictorsF',z(end),'Beta',betaHat);