%% fGn.m

N = 10;
NN = 2^N+1;
H1 = 0.3;
H2 = 0.8;
q = 0.9;
M = 100;

X1 = choleskyFBM(H1,NN,M);
X2 = choleskyFBM(H2,NN,M);

plot_realizations(X1,X2,'c');