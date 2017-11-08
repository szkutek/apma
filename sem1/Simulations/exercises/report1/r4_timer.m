function [t1,t2,t3] = r4_timer(a,b,s,m,M,N)

x1=tic;
X1 = stabrnd(a,b,s,m,N); % CMS
t1=toc(x1);

x2=tic;
X2 = gclt(a,m,M,N); % a>1 for Pareto?
t2=toc(x2);

x3=tic;
X3 = seriesstab(a,m,M,N); % series representation beta=0
t3=toc(x3);