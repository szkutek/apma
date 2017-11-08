H = 0.8;
L = 1024;


tic;
for i = 1:1000
%  wfbm(H,L);
  cumsum([0, fGn(H,10)]);
end
toc