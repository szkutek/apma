
a=[0.5, 1.5];
%b=[-1, 0, 0.5];
b=0;
s=1;
%m=[0, 2];
m=[0];
%N=[100, 1000];
N=[100];
M = [10, 100]; % number of Pareto used in GCLT and uniform r.v. used in seriesstab

i=1;
param = zeros(4,5);
for ia = a(2)
  for im = m
    for iM = M(1)
      for iN = N
        [X1,X2,X3] = r2_generate_rv(ia,b,s,im,iM,iN);
        
        param(i,:) = [i, ia, im, iM, iN];
        save(['x1_',num2str(i),'.txt'],'X1','-ascii');
        save(['x2_',num2str(i),'.txt'],'X2','-ascii'); 
        save(['x3_',num2str(i),'.txt'],'X3','-ascii');

        r3_pdf(ia,b,s,im,iM,iN,X1,X2,X3);
        
        [mean(X1), mean(X2), mean(X3)]
        i=i+1;
      end
    end
  end
end
saveas(1,"1pdf.eps");