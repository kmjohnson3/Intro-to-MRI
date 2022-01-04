function [MOutput, BOutput] = bloch_solver( B, time, freq, T1, T2, M0)
% This is simple Rk4 solution to the Bloch Equations.
%
% Inputs:
%   B          -- Magentic Field (N x 3) (T)
%   time       -- Time of each point in waveforms (s)
%   T1         -- Longitudinal relaxation times (s)
%   T2         -- Transverse relaxation times (s)
%   Freq Offset-- Off center frequency in Hz
%   M0         -- Initial state of magnetization (not equilibrium magnetization)
% Outputs:
%   MOutput -- Magnetization for each position in time
%   BOutput -- Magnetic field for each position in time (interpolated)

% Assume protons
GAM = 42.58e6*2*pi;

% Storage for solution
MxOutput = [];
MyOutput = [];
MzOutput = [];

% Convert frequency to rads/s
act_freq = 2*pi*freq;

%Convert to B1
Bx =  B(:,1);
By =  B(:,2);
Bz =  B(:,3) + act_freq/GAM; %a frequency offset is a Bz offset

%Create a spline for interpolation
Bs = spline(time,GAM*[Bx(:)'; By(:)'; Bz(:)']);

%Initialize
Mag = M0;

count = 1;

%Runge-Kutta PDE Solution
tvals = linspace(min(time),max(time),length(time));
dt = tvals(2) - tvals(1);
for t1 = tvals
    
    m1 = Mag;
    b = ppval(Bs,t1);
    k1 = [  -1/T2    b(3)      -b(2);
        -b(3)      -1/T2        b(1);
        b(2)       -b(1)      -1/T1]*m1 + [0; 0; 1/T1];
    
    t2 = t1 + dt/2;
    b = ppval(Bs,t2);
    m2 = Mag + k1*dt/2;
    k2 = [  -1/T2    b(3)      -b(2);
        -b(3)      -1/T2        b(1);
        b(2)       -b(1)      -1/T1]*m2 + [0; 0; 1/T1];
    
    t3 = t1 + dt/2;
    m3 = Mag + k2*dt/2;
    k3 = [  -1/T2    b(3)      -b(2);
        -b(3)      -1/T2        b(1);
        b(2)       -b(1)      -1/T1]*m3 + [0; 0; 1/T1];
    
    
    t4 = t1 + dt;
    b = ppval(Bs,t2);
    m4 = Mag + k3*dt;
    k4 = [  -1/T2    b(3)      -b(2);
        -b(3)      -1/T2        b(1);
        b(2)       -b(1)      -1/T1]*m4 + [0; 0; 1/T1];
    
    Mag = Mag + dt/6*(k1 + 2*k2 + 2*k3 + k4);
    
    % Save output of magnetization
    MOutput(:,count)= Mag;
    
    % Save Output of magnetic field
    BOutput(:,count)= b;

    count = count+1;
end



