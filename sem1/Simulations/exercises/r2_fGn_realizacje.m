K=15;
%% fGn.m

N = 10;
H = 0.2;
q = 0.9;
M = 100;

X = zeros(2^N + 1, M);
for i=1:M
  X(:,i) = [0, cumsum(fGn(H,N))];
end

figure;

plot(X); hold on;
title([num2str(M),' realizations of Gaussian \alpha-stable process'], "fontsize", K+5);
axis([0 length(ql)]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);


figure;

ql = quantilelines(X,[q]); % empirical quantile line
f = (1:2^N).^H * norminv(q,0,1); % analytical quantile line

plot(X); hold on;
p1=plot(ql, 'r', 'LineWidth', 25); 
p2=plot(f, 'b', 'LineWidth', 5);
legend([p1,p2],'empirical', 'analytical');

title(['Quantile lines 0.9 for ', num2str(M),' realizations of Gaussian \alpha-stable process'], "fontsize", K+5);
axis([0 length(ql)]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);



figure;

p1=plot(ql, 'r'); hold on;
p2=plot(f, 'b');
legend([p1,p2],'empirical', 'analytical');

title('Quantile lines 0.9', "fontsize", K+5);
axis([0 length(ql)]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);


