%% Hill estimator
% n=10000;
% al=0.5; lam=2; 
% U=unifrnd(0,1,1,n);
% X=lam*(U.^(-1/al) - 1);
% 
% sX=sort(X,'descend');
% 
% gam=1/al;
% 
% m=2:n;
% est=zeros(1,length(m));
% for k=2:n
%     est(k-1) = 1/k * sum(log(sX(1:k-1))) - log(sX(k));
% end
% plot(m,est);
% 
% al_est = 1/est(round(n/4))

%% CLT
n=10; % how many unif are used to generate normal
N=1000; % number of normal numbers
X=unifrnd(0,1,N,n);
m=1/2; s=1/12;

Y=(sum(X,2)-n*m) / (sqrt(n)*sqrt(s));
%plot(Y);
%ksdensity(Y)
t=linspace(min(Y),max(Y),1000);
ksden = kernel_density(t',Y);
plot(t,ksden)


%[H,p]=jbtest(Y) % p < 0.05 -> Y not Gaussian
