
a=1.5;
b=0;
s=1;
m=0;
%N=[100, 1000];
N=[1,100,1000];
M = [10, 100]; % number of Pareto used in GCLT and uniform r.v. used in seriesstab


times=zeros(4,5);
K=100;
T1=zeros(6,K);
T2=zeros(6,K);
T3=zeros(6,K);
for k = 1:K
  i=1;
  for iN = N
    for iM = M
      [t1,t2,t3]=r4_timer(a,b,s,m,iM,iN);
      T1(i,k)=t1;
      T2(i,k)=t2;
      T3(i,k)=t3;
      i=i+1;
    end
  end
end
times = [ mean(T1,2), mean(T2,2), mean(T3,2) ];

printf ("%.4e %.4e %.4e\n", times);