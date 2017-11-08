% Comparison of alpha-stable random variable generators
% CMS method, GCLT (with Pareto), series representation

% for several values of a,b,s,m simulate the alpha-stable r.v. 
% and compare the parameters
% speed of the generators
% accuracy of the generators

a=1.8;
b=0;
s=1;
m=0;
N=10000;

M = 100; % number of Pareto used in GCLT and uniform r.v. used in seriesstab
lam = 1;


X1 = stabrnd(a,b,s,m,N); % CMS

X2 = gclt(a,m,M,N); % a>1 for Pareto?

X3 = seriesstab(a,m,M,N); % series representation beta=0


X1 = X1';X2 = X2';X3 = X3';
save('x1.txt','X1','-ascii');
save('x2.txt','X2','-ascii');
save('x3.txt','X3','-ascii');

%plot(X1,'b*',X2,'r*',X3,'g*');
%plot(X1,'b',X2,'r',X3,'g');
plot(X1,'bo',X2,'r^',X3,'ks');
xlabel('number of realization', "fontsize", 20);
ylabel('\alpha-stable r. v.', "fontsize", 20);
title([num2str(iN),' realizations of \alpha-stable r. v. with \alpha=',num2str(ia)], "fontsize", 20);
legend("CMS","GCLT","SERIES");

printf("CMS: %f\nGCLT: %f\nSeries: %f\n", mean(X1), mean(X2), mean(X3));