function h = AV_est(X)
L = length(X);
m = floor(L/10);
AV_m = zeros(1,m);
for i = 1:m
    X_m = zeros(1,floor(L/i));
    for k = 1:floor(L/i)
        X_m(k) = (1/i)*sum(X((k-1)*i+1:k*i));
    end
    AV_m(i) = (i/L)*sum(abs(X_m - mean(X)));  
end
plot(log(1:m),log(AV_m),'*');
a = polyfit(log(1:m),log(AV_m),1);
h = a(1) + 1;
