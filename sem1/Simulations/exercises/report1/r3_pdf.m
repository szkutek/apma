function plt = r3_pdf(a,b,s,m,M,N, X1,X2,X3)
X=[X1;X2;X3];

t=linspace(min(X),max(X),N);
d1 = kernel_density(t',X1,10);
d2 = kernel_density(t',X2,10);
d3 = kernel_density(t',X3,10);

figure;
hold on;
plot(t,d1,'bo',t,d2,'r^',t,d3,'ks' );
%plot(t,d1,'b',t,d2,'r',t,d3,'k'); 
%subplot(2,1,i); hold on;
%plot(X1,'bo',X2,'r^',X3,'ks');
xlabel('x', "fontsize", 20);
ylabel('f(x)', "fontsize", 20);
title(['Pdf of \alpha-stable r. v. with \alpha=',num2str(a)], "fontsize", 20);
legend("CMS","GCLT","SERIES");