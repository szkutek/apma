% GCLT
a= 3;
l = 3;
n=1000;
X = gclt(n,1000,a,l);
X = X';
save('data.txt','X','-ascii');
% plot(X);
% c = l*((2*gamma(a)*sin(pi*a/2))/pi)^(-1/a) 
% an = c * n^(1/a);

% [h,p] = jbtest(X)
% p should be in [0.001, 0.50]

%%
u = rand(1,10);
u(u>0.5) = 1;
u(u<=0.5)=-1;
u