K=15;
%% fGn.m

N = 10;
H1 = 0.3;
H2 = 0.8;
q = 0.9;
M = 100;

X1 = zeros(2^N + 1, M);
X2 = zeros(2^N + 1, M);
for i=1:M
  X1(:,i) = [0, cumsum(fGn(H1,N))];
  X2(:,i) = [0, cumsum(fGn(H2,N))];
end

plot_realizations(X1,X2,'dh');
