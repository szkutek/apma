function y = stablemotion(alpha, beta, T, I, N)

y = zeros(I+1, N);
tau = T/I;
for n = 1:N
  y(:,n) = cumsum( [0, stabrnd(alpha, beta, tau^(1/alpha), 0, I)] );

end