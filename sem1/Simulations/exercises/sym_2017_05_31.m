%H=0.2;
%T=1000;
%N=1000;
%printf("3-sigma is %g\n", T^H*3);

H=0.8; % 0.2, 0.5, 0.8
T=1000;
N=1;

%X = choleskyFBM(H,T,N);
%%plot(X);
%
%Y = diff(X);
%%plot(Y);

%%autocorr(Y); % MATLAB

Z = fGn(0.8, 20); % (H, 2^N)
plot(Z);