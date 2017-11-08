
% multivariate alpha-stable r.v.
vals =[ 0.0000         1.8274    
     180.00         8.8586    
     189.00         4.4385    
     351.00        0.48561  ];
angles = vals(:,1) * pi/180;
S=zeros(4,2);
for i = 1:length(angles)
  x=cos(angles(i));
  y=sin(angles(i));
  S(i,:) = [x,y];
end
G = vals(:,2);
mu0 = [0.4428445028    0.01989942900];

Z=stablevector(1.87, S, G, mu0, 500);
%plot(Z(:,1),Z(:,2),'*')
%save('mvs.txt','Z','-ascii');
hist3(Z);