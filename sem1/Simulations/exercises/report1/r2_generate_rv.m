function [X1,X2,X3] = r2_generate_rv(a,b,s,m,M,N)


X1 = stabrnd(a,b,s,m,N); % CMS

X2 = gclt(a,m,M,N); % a>1 for Pareto?

X3 = seriesstab(a,m,M,N); % series representation beta=0


X1 = X1';X2 = X2';X3 = X3';