H=0.8;
alpha=1.2;
m=256;
M=600;
C=2;
N=2^12-M;
n=1;

% H < 1/alpha
X1 = fftlfsn(H,0.8,m,M,C,N,n);
%%%figure(1);
%%%autocorr(X1); %MATLAB


%% H > 1/alpha
res = fftlfsn(H,1.8,m,M,C,N,n);
%%%figure(2);
%%%autocorr(X2); %MATLAB