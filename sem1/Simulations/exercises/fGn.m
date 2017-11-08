function Y = fGn(H,N)
%
% simulates a trajectory of lenght 2^N of a fractional Gaussian noise
% for given 0< H_<1 by means of the Davies and Harte method
%
% input:
% H <- self-similarity parameter
% N <- 2^N is the length of the trajecory
% 
% output:
% Y <- trajectory of the fractional Gaussian noise
% ***************************************************************************
% Literature: 
% 1. D. Caccia, D. Percival, M. Cannon, G. Raymond, and J. Bassingthwaighte. 
% Analyzing exact fractal time series: evaluating dispersional analysis and 
% rescaled range methods. Phys. A, 246:609 632, 1997.
% 2. R. Davies and D. Harte. Test for Hurst effect. Biometrika, 1:95 101, 1974.
% ***************************************************************************
% Written by Krzysztof Burnecki, 08.10.2009, Krzysztof.Burnecki@pwr.edu.pl.
%
% usage:
% Y = fGn(H,N);
%

N = 2^N;
M = 2*N;

t1 = 0:M/2;
t2 = M/2-1:-1:1;

V = zeros(1,M);


gamma = gam([t1,t2],H);

Sc = fft(gamma,M);
S = real(Sc(1:M/2+1));


if any(S<0)
   error('Błąd w algorytmie');
end;

%randn('state',sum(100*clock));


W = randn(1,M);
V(1) = sqrt(S(1))*W(1);
V(2:M/2) = sqrt(S(2:M/2)/2).*(W(2:2:M-2)+i*W(3:2:M-1));
V(M/2+1) = sqrt(S(M/2+1))*W(M);
V(M/2+2:end) = conj(V(M/2:-1:2));
Yc = 1/sqrt(M)*fft(V,M);
Y = real(Yc(1:N));

%plot(Y);

function g = gam(t,H)

g = 1/2*(abs(t+1).^(2*H)-2*abs(t).^(2*H)+abs(t-1).^(2*H));