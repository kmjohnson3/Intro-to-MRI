% Example : T1 recovery from 0 magnetization
 M0 = [0; 0; 0];
 time = 0:1e-3:2;
 B = zeros(length(time),3);
 freq = 0;
 T1 = 1; %s
 T2 = 1; %s
 [Mout,Bout] = bloch_solver( B, time, freq,T1, T2, M0);
 figure
 plot(time,Mout)
 ylabel('Magnetizaton [a.u.]');
 xlabel('Time [s]');
 legend('Mx','My','Mz')
 
 % Example : T2 decay
 M0 = [1; 0; 0];
 time = 0:1e-4:2;
 B = zeros(length(time),3);
 freq = 100;
 T1 = 1; %s
 T2 = 0.1; %s
 [Mout,Bout] = bloch_solver( B, time, freq,T1, T2, M0);
 figure
 plot(time,Mout)
 ylabel('Magnetizaton [a.u.]');
 xlabel('Time [s]');
 legend('Mx','My','Mz')
 
  
 % Example : RF Excite starting from thermodynamic equilibrium
 M0 = [0; 0; 1];
 time = 0:1e-5:0.1;
 B = zeros(length(time),3);
 T = 8e-3; %8ms pulse
 flip = 30; %30 degree flip
 B( (time>=1e-3) & (time<=1e-3+T),1)= (30/360)/T/42.58e6;
 freq = 0;
 T1 = 1; %s
 T2 = 0.1; %s
 [Mout,Bout] = bloch_solver( B, time, freq,T1, T2, M0);
 figure
 plot(time,Mout)
 ylabel('Magnetizaton [a.u.]');
 xlabel('Time [s]');
 legend('Mx','My','Mz')