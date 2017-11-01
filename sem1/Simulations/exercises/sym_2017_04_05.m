X=seriesstab(1.5,10,1000);
% plot(X);

X = X';
save('seriesstab.txt','X','-ascii');