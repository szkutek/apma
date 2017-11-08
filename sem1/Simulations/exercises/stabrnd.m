function y = stabrnd(a, b, s, m, N)
% CMS algorithm
% for a != 1

U = rand(1,N) * pi - pi/2;
W = -log(rand(1,N));

B = atan(b * tan(pi*a/2) ) / a;
S = (1 + b^2 * ( tan(pi*a/2) )^2 )^(0.5/a);

X = S * sin(a*(U+B))./(cos(U)).^(1/a) .* ( cos( U-a*(U+B) )./W ).^((1-a)/a);

y = s*X+m;