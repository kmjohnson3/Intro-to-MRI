clear
clc
close all

%Settable parameters
TBW = 8; % time bandwidth product (unitless)
T = 2e-3; %total time of pulse (s)
thickness = 0.1; % selection thickness (m)
gamma = (42.58e6); % gamma (has to be this since bloch sim doesn't take input)
flip = 90; % flip angle (degrees)

% 8us spacing is reasonable
dT = 8e-6;

% Intial state of magnetization
M0 = [0; 0; 1];

% Time
time = 0:dT:T;

% Sinc pulse with 2 sidelobes
B1  = sinc(linspace(-TBW/2,TBW/2,numel(time)))';

%Get the BW
BW = TBW/(max(time));

% Plot frequency content of B1 pulse
N = numel(B1);
SamplingBW = 1/(dT);
f = linspace(-SamplingBW/2,SamplingBW/2,10000);
figure
dft_of_b1 = abs(fftshift(fft(B1,10000)));
ideal_b1 = double(abs(f) < BW/2);
dft_of_b1 = dft_of_b1*(ideal_b1(:)'*dft_of_b1(:))/(dft_of_b1(:)'*dft_of_b1(:)); % just to scale nicely
plot(f,dft_of_b1);
hold on
plot(f,ideal_b1)
xlim([-BW BW]);
ylim([0 1.2]);
xlabel('Frequency [Hz]')
ylabel('Value [a.u.]');
title(['Fourier Tranform of B1 Pulse (TBW=',num2str(TBW),',BW=',num2str(BW),')'])

% Constant gradient
Gamp = BW / ( gamma*thickness); 
G  = Gamp*ones(numel(time),1);

% Add rephasing gradient and som zero values at the end
G = [G; -0.5*G; 0.0*G];
B1= [B1; 0*B1; 0*B1];
time = dT*(0:numel(G)-1)';

% Calculate over +/- 10cm
zloc = linspace(-thickness,thickness,101);

% Offset frequency
freq = 0;
T1 = 100000;
T2 = 100000;

% set flip to 90 
B1 = B1*(flip/180*pi)/(2*pi*42.58e6*sum(real(B1)*dT));

figure
subplot(121)
plot(time,B1);
xlabel('Time [s]')
ylabel('B_1 [T]')
xlim([min(time) max(time)])
subplot(122)
plot(time,G);
xlabel('Time [s]')
ylabel('G [T/m]')
xlim([min(time) max(time)])

for z_index = 1:numel(zloc)
    % Setup magnatic field
    B(:,1) = real(B1);
    B(:,2) = imag(B1);
    B(:,3) = G.*zloc(z_index);
    
    % Run simulator
    [Mout,Bout] = bloch_solver( B, time(:),freq(:),T1, T2, M0);
    % Mx is [1 (freq) x 101 (z) x 251 (time)]
    Mx(z_index,:) = Mout(1,:);
    My(z_index,:) = Mout(2,:);
    Mz(z_index,:) = Mout(3,:);
end

figure
plot(zloc,squeeze(abs(Mx(:,end)+1i*My(:,end))))
xlabel('Z Location [m]');
ylabel('M_x_y [1/M_0]');


figure
title('M_x_y During RF');
imagesc(time,zloc,squeeze(abs(Mx(:,:)+1i*My(:,:))))
ylabel('Z Location [m]');
xlabel('Time [s]');
title('M_x_y')
colorbar

figure
imagesc(time,zloc,squeeze(angle(Mx(:,:)+1i*My(:,:))))
ylabel('Z Location [m]');
xlabel('Time [s]');
title('\angle{M_x_y} During RF');
colorbar

figure
title('M_z During RF');
imagesc(time,zloc,squeeze(Mz(:,:)))
ylabel('Z Location [m]');
xlabel('Time [s]');
title('M_z')
colorbar
