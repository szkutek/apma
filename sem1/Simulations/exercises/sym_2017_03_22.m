a=0.5;
b=0;
s=1;
m=0;
N=1000;

X = stabrnd(a,b,s,0,N);
X=X';
Y = stabrnd(a,b,s,2,N);
Y=Y';
% multivariate alpha-stable r.v.
Z=[X,Y];
save('mvs.txt','Z','-ascii');

%%
% 
% X = csvread('kgh.csv',1,1);
% 
% data=X(:,1);
% 
% returns=data(2:end)./data(1:end-1)-1;
% plot(returns);
% 
% save('kgh.txt','data','-ascii');