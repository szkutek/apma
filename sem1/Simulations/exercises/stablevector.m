function X = stablevector(alpha, S, Gamma, mu0, N)

[n,d] = size(S);
X = zeros(N,d);

for i = 1:N
   Z = stabrnd(alpha, 1,1,0,n);
   for k = 1:d
       X(i,k) = sum(Gamma.^(1/alpha) .* Z' .* S(:,k) );
   end
   X(i,:) = X(i,:) + mu0;
end