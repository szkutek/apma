function y = gclt(n,N,alpha,lambda)
mu=lambda/(alpha-1);
y = zeros(1,N);
for i=1:N
    X = lambda * (rand(1,n).^(-1/alpha)-1);
%     y(i) = (sum(X) - n*mu) / n^(1/alpha); % stable
    y(i) = (sum(X) - n*mu) / n^(1/2); % normal
end
