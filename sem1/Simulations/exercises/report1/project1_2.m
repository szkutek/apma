% Comparison of alpha-stable random variable generators
% CMS method, GCLT (with Pareto), series representation

% for several values of a,b,s,m simulate the alpha-stable r.v. 
% and compare the parameters
% speed of the generators
% accuracy of the generators



save('x1.txt','X1','-ascii');
save('x2.txt','X2','-ascii');
save('x3.txt','X3','-ascii');

plot(X1,'bo',X2,'r^',X3,'ks');
xlabel('number of realization', "fontsize", 20);
ylabel('\alpha-stable r. v.', "fontsize", 20);
title('100 realizations of \alpha-stable r. v.', "fontsize", 20);
legend("CMS","GCLT","SERIES");
%plot(X1,'b',X2,'r',X3,'g');

[mean(X1), mean(X2), mean(X3)]