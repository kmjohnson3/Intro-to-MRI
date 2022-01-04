function [time, Mout] = bloch_nutation_solver( event_list, M0, T1, T2, freq )

% Inputs:
%   event_list -- Special structure with entries
%            .excite_flip  flip angle of rotation
%            .excite_phase phase of excite degrees
%            .recovery_time time after excite to recover 
%            .spoil (if 'true' this set the Mxy to zero at the recovery)
%   T1         -- Longitudinal relaxation times (s)
%   T2         -- Transverse relaxation times (s)
%   Freq Offset-- Off center frequency in Hz
%   M0         -- Initial state of magnetization (not equilibrium magnetization)
% Outputs:
%   time -- Magnetization for each position in time
%   BOutput -- Magnetic field for each position in time (interpolated)

% Initialize
count = 1;
time(1) = 0;
Mout(1,:) = M0;

M=M0;

% Go through the event_list
for pos = 1:numel(event_list)
    
    theta = event_list{pos}.excite_phase;
    alpha =  event_list{pos}.excite_flip;
    T = event_list{pos}.recovery_time;
    spoil = event_list{pos}.spoil;
    
    % Excite
    Rz = [cosd(theta) sind(theta) 0;
         -sind(theta) cosd(theta) 0;
          0  0 1]; 
    Rx = [1 0 0;
         0 cosd(alpha) sind(alpha);
         0 -sind(alpha) cosd(alpha)];
    M = inv(Rz)*Rx*Rz*M;
    
    % Relaxation (Transverse)
    if spoil
        Mxy = 0;
    else
        Mxy = M(1) + 1i*M(2);
        Mxy = Mxy*exp( 2i*pi*freq*T)*exp(-T/T2);
    end
       
    % Relaxation (Longitudinal)
    Mz = M(3);
    Mz = 1 + (Mz - 1)*exp(-T/T1);
    
    % Put back into [Mx; My; Mz] vector
    M = [real(Mxy); imag(Mxy); Mz];
    
    % Store for output
    count = count+1;
    time(count) = time(count-1)+T;
    Mout(count,:) = M;
end
    
      
    
    