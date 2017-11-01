a=1;
b=0;
s=1;
m=0;
N=10000;

X = stabrnd(a,b,s,m,N);
% Y = stabrnd(1.5, 1,1, 2,10000);
% t=5;
% [f1,x1] = ksdensity(X,-t:0.01:t);
% [f2,x2] = ksdensity(Y,-t:0.01:t);
% plot(x1,f1);hold on;
% plot(x2,f2);
% X = stabrnd(1.5,-1,1,-2,10000);

%%

% sX=sort(X(X>0),'descend');
% n = length(sX);
% gam=1/a;
% 
% m=2:n;
% est=zeros(1,length(m));
% for k=2:n
%     est(k-1) = 1/k * sum(log(sX(1:k-1))) - log(sX(k));
% end
% plot(m,est);
% 
% a_est = 1/est(round(n/4))