function age = avm(data)
% Absolute value method (a block aggregation method)
L = length(data);
M = floor(L/10);
m = 1:M;
X = reshape(data,[L,10])
