X = stablemotion(1.6,0,100,1000,100);
%plot([0:0.1:100], X); hold on;
plot(X); hold on;
%plot(stabrnd(0.8,-1,1,0,1000));

%X = stabrnd(0.8,-1,1,0,1000);
quantilelines(X,[0.05, 0.95]);