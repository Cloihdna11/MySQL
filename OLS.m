clc;
clear;
%data = importdata('SP500_DP_dVIX_198602_2018121.csv');
data = importdata('SP500_DP_dVIX_198602_2018121.csv');

Y=data.data(:,2); % Mkt return
X=data.data(:,3); %vix
steps=size(Y,1); % 
h=10;% window size
p=1; %number of regressors 
j=1; 
k=1; 
error = [];
count=0;
for i=1:j:steps-h   
    y=Y(i:9+i,k);
    x=[ones(10,1),X(i:9+i,1)];
   % [b bint r rint stats]=regress(Y(i:9+i,k),[ones(10,1),X(i:9+i,1)]);
    [b bint r rint stats]=regress(y,x);
   % output args b--coeff. estimates( dbl); bint--lower and upper confidence bounds                                                                  
   % for coeff's estimates(matrix); r--residuals(vector) p-by-1 n is num of
   % p is number of predictors; rint--Intervals to diagnose outfliers n-by-2 matrix. if in
   % rint(i:) does not contain zero, then suggests an outlier. stats--model
   % statistics, vector includes the R^2 stat, the F-stat, its p-value and
   % an estimate of it's error variance. X must include a column of ones
   % relationship between response variable and predictor variables. k--number of columns = 1  
    count=count+1;
    Alpha(count,k)=b(1);
    Beta(count,k)=b(2);   % for constant. F-test looks at the significant linear regression

    R_Squared(count,k)=stats(1); 
    %error(:,i,k)=r(:,1); 
    CI_Alpha(count,:,k)=bint(1,:); % upper bound confidence interval
    CI_Beta(count,:,k)=bint(2,:);  % lower bound CI
    if CI_Alpha(count,1,k)*CI_Alpha(count,2,k)<0;           
        Significance_Alpha(count,k)=0;                  
    else
        Significance_Alpha(count,k)=1;
    end
    if CI_Beta(count,1,k)*CI_Beta(count,2,k)<0;
        Significance_Beta(count,k)=0;
    else
        Significance_Beta(count,k)=1;
    end  
    
    error=[error;r(end,1)];
    
   
  
end
RMSE = sqrt(mean(error.^2));  % Root Mean Squared Error
subplot(3,2,1),plot(Alpha); legend('Rolling Alpha')
subplot(3,2,2),plot(Beta); legend('Rolling Beta')
