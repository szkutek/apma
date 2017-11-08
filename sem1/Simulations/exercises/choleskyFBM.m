function X = choleskyFBM(H, T, N)

Sigma = zeros(T); % covariance matrix
for t = 1:T
  for s = 1:T
    Sigma(t,s) = 0.5 * ( t^(2*H) + s^(2*H) - abs(t-s)^(2*H) );
  end
end

C = chol(Sigma);
Z = randn(T, N);

X = C' * Z;
X = [ zeros(1,N); X];