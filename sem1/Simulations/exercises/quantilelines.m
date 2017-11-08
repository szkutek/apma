function ql = quantilelines(X,q)
% trajectories are in columns
% e.g. q = [0.05, 0.95], q = [0.1, 0.2, ..., 0.9] (at least one elem in vector)

[L,N] = size(X);
ql = zeros(L, length(q));

for i = 1:L
  xs = sort( X(i,:) );
  ql(i,:) = xs( floor(q*N) );
end

  