function y = OULamperti(a,b,T1,T2,I,N)
%a=2;
%b=0;
%T1=-10;
%T2=10;
%I=1000;
%N=10;

tau = (T2-T1)/I;
y=zeros(I+1, N);
H = 1/a;
for i = 1:N
  t = exp( T1:tau:T2 );
  ksi = zeros(1,I);
  X = zeros(I,1);
  for k = 1:I
    ksi(k) = stabrnd(a,b,(exp(T1+k*tau)-exp(T1+(k-1)*tau))^H,0,1);
    ksi(k) = stabrnd(a,b,(t(k+1)-t(k))^H,0,1);
%    X(k+1) = X(k) + ksi(k);
  end
  X = cumsum( [ stabrnd(a,b,(exp(T1))^H,0,1), ksi ] );
  y(:,i) = t.^(-H) .* X;
end 

%plot(y);