N = 10;
H = 0.8;
q = 0.9;
M=100;
X = zeros(2^N + 1, M);

for i=1:M
  X(:,i) = [0, cumsum(fGn(H,N))];
end

ql = quantilelines(X,[q]);

f = (1:2^N).^H * norminv(q,0,1); % analytical quantile line

plot(X); hold on;
p1=plot(ql, 'r', 'LineWidth', 25); hold on;
p2=plot(f, 'b', 'LineWidth', 5);
legend([p1,p2],'quantile line', 'analytical');
title('Realizations of Gaussian \alpha-stable process',"fontsize", 20);
axis([0 length(ql)]); 
ylabel('X(t)', "fontsize", 20);
xlabel('t', "fontsize", 20);