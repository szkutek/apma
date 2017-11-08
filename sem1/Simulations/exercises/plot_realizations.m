function plot_realizations(X1,X2,filename)

K=15;

N = 10;
H1 = 0.3;
H2 = 0.8;
q = 0.9;
M = 100;


F1=figure; % increments

subplot(1,2,1);
plot(diff(X1)); hold on;
title([num2str(M),' increments for H=',num2str(H1)], "fontsize", K+5);
axis([0, 2^N + 1,-6,6]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

subplot(1,2,2);
plot(diff(X2)); hold on;
title([num2str(M),' increments for H=',num2str(H2)], "fontsize", K+5);
axis([0, 2^N+1,-6,6]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

filename1 = [filename, '1.eps'];
saveas(F1,filename1,'epsc');



%clf;
F2=figure;

subplot(1,2,1);
plot(X1); hold on;
title([num2str(M),' realizations with H=',num2str(H1)], "fontsize", K+5);
axis([0, 2^N + 1]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

subplot(1,2,2);
plot(X2); hold on;
title([num2str(M),' realizations with H=',num2str(H2)], "fontsize", K+5);
axis([0, 2^N+1]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

filename1 = [filename, '2.eps'];
saveas(2,filename1,'epsc');


%clf; 
F3=figure;

subplot(1,2,1);
ql1 = quantilelines(X1,[q]); % empirical quantile line
f1 = (1:2^N).^H1* norminv(q,0,1); % analytical quantile line
plot(X1); hold on;
p1=plot(ql1, 'r', 'LineWidth', 5); 
p2=plot(f1, 'b', 'LineWidth', 5);
leg = legend([p1,p2],'empirical', 'analytical');
set(leg, 'FontSize', K);
set(leg, 'Location', 'southwest');
title([num2str(M),' realizations with H=',num2str(H1)], "fontsize", K+5);
axis([0, 2^N+1]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

subplot(1,2,2);
ql2 = quantilelines(X2,[q]); % empirical quantile line
f2 = (1:2^N).^H2 * norminv(q,0,1); % analytical quantile line
plot(X2); hold on;
p1=plot(ql2, 'r', 'LineWidth', 5); 
p2=plot(f2, 'b', 'LineWidth', 5);
leg = legend([p1,p2],'empirical', 'analytical');
set(leg, 'FontSize', K);
set(leg, 'Location', 'southwest');
title([num2str(M),' realizations with H=',num2str(H2)], "fontsize", K+5);
axis([0, 2^N+1]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

filename1 = [filename, '3.eps'];
saveas(F3,filename1,'epsc');



%clf; 
F4= figure;

subplot(1,2,1);
p1=plot(ql1, 'r'); hold on;
p2=plot(f1, 'b');
leg = legend([p1,p2],'empirical', 'analytical');
set(leg, 'FontSize', K);
set(leg, 'Location', 'southeast');
title('Quantile line 0.9', "fontsize", K+5);
axis([0, 2^N+1]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

subplot(1,2,2);
p1=plot(ql2, 'r'); hold on;
p2=plot(f2, 'b');
leg = legend([p1,p2],'empirical', 'analytical');
set(leg, 'FontSize', K);
set(leg, 'Location', 'southeast');
title('Quantile line 0.9', "fontsize", K+5);
axis([0, 2^N+1]); 
ylabel('X(t)', "fontsize", K);
xlabel('t', "fontsize", K);

filename1 = [filename, '4.eps'];
saveas(F4,filename1,'epsc');