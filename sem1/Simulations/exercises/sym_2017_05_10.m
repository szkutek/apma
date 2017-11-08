
data = importdata('findata.txt');
x=data(:,1);
y=data(:,2);
%figure;
%plot(x); hold on;
%figure;
%plot(y);

%hist(x);
%figure;
%hist(y);
hist3(data);

%printf('skewness(x) = %g \n',skewness(x));
%printf('skewness(y) = %g \n',skewness(y));
%printf('corr(x,y) = %g \n',corr(x,y));
%
%plot(x,y,'*');


