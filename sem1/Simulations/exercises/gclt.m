function y = gclt(alpha,m,M,N)
lambda = 1;
mu=lambda/(alpha-1);
%lambda = mu * (alpha-1);
y = zeros(1,N);
for i=1:N
    X = lambda * (rand(1,M).^(-1/alpha)-1);
    y(i) = (sum(X) - M*mu) / M^(1/alpha); % stable
%    y(i) = (sum(X) - M*mu) / M^(1/2); % normal
end
%y = y-mu + m;
