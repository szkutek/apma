N = 10;
NN = 2^N+1;
H1 = 0.3;
H2 = 0.8;
M = 100;



M=1000000;
for H=[H1,H2];
     
  printf('M = %g, ',M);
  printf('H = %g\n',H);

  tic;
  for i=1:M
    [0, cumsum(fGn(H,N))];
  end
  toc

  tic;
  choleskyFBM(H,NN,M);
  toc
end