function y = seriesstab(alpha,M,N)

y=zeros(1,N);
for i=1:N
    E=rand(1,M);
    E(E<0.5)=-1;
    E(E>0.5)=1;
    G=-cumsum(log(rand(1,M)));
    y(i)=sum(E .* G.^(-1/alpha));
end