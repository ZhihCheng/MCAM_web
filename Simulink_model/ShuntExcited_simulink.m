clc;clear;

% 設定參數（註解掉的部分）
% L = 0.013242
% R = 3.2645
% J = 0.01829
% B = 0.019
% Ke = 1.1895
% Kt = 1.1895
% simulation_time = 150

% 執行 Simulink 模型模擬
out = sim("ShuntExcited_model");

%% Data Loading

tl2 = out.Tl2;
f2 = size(tl2);

% clear datas 
torque2 = 0;
x12 = 0;
y12 = 0; y22 = 0; y32 = 0; y42 = 0; y52 = 0; y62 = 0;

switch LoadMode   % mode ( 1:ramp load , 2:stair load )

    case 1  

        i = 1;
        while 1
            if tl2(i) > 0.01
               s = i;
               break
            end
            i = i+1;
        end
        torque2 = out.Tl2(s:f2(1));
        x12 = out.omega2(s:f2(1));
        % y12 = out.omega2(s:f2(1));
        y22 = out.Eff2(s:f2(1));
        y32 = out.Pin2(s:f2(1));
        y42 = out.Pout2(s:f2(1));
        y52 = out.Vs(s:f2(1));
        y62 = out.Ia2(s:f2(1));
        case 2

        tl_pre2 = 0;
        j = 1;
        for i = 1:f2(1)           
            if tl2(i) > tl_pre2
                torque2(j,1) = tl2(i-1);
                x12(j,1) = out.omega2((i-1),1);
                % y12(j,1) = out.omega2((i-1),1);
                y22(j,1) = out.Eff2((i-1),1);
                y32(j,1) = out.Pin2((i-1),1);
                y42(j,1) = out.Pout2((i-1),1);
                y52(j,1) = out.Vs((i-1),1);
                y62(j,1) = out.Ia2((i-1),1);
                j = j+1;
            end
            tl_pre2 = tl2(i);
        end
end

%% Plot
% plot TN curve

% figure(1);

fig = figure('Visible', 'off');
set(gcf, 'Position', [200, 300, 1000, 500]); % [left, bottom, width, height]
clf;

% Create empty axis system with 4 y axis by calling:
% handle = maxis(number of axis, y-spacing between outside lines)
h = myaxisc(5,0.10,[0.1,0.1,0.8,0.8]); % Specify position

% Call plot and specify y-axis number using method h.p(nr). For creating a
% legend later, we need to assign the handles returned by plot to p.
switch PlotMode

    case 1  
        p(1) = plot(h.p(1),x12,torque2,'b','LineWidth',1.2);
        p(2) = plot(h.p(2),x12,y22,'Color',[0.4660 0.6740 0.1880],'LineWidth',1.2);
        p(3) = plot(h.p(3),x12,y62,'Color',[0.3010 0.7450 0.9330],'LineWidth',1.2);
        p(4) = plot(h.p(4),x12,y52,'r','LineWidth',1.2);
        p(5) = plot(h.p(5),x12,y32,'m','LineWidth',1.2);
        print("case1");

    case 2
        p(1) = plot(h.p(1),x12,torque2,'b-*','LineWidth',1.1);
        p(2) = plot(h.p(2),x12,y22,'-*','Color',[0.4660 0.6740 0.1880],'LineWidth',1.1);
        p(3) = plot(h.p(3),x12,y62,'-*','Color',[0.3010 0.7450 0.9330],'LineWidth',1.1);
        p(4) = plot(h.p(4),x12,y52,'r-*','LineWidth',1.1);
        p(5) = plot(h.p(5),x12,y32,'m-*','LineWidth',1.1);
        print("case2");

end

for i = 1:5
    h.autoy(i);
end

% Additional methods to modify appearance, scaling and so on:

%h.ylim(3,[95,105]); % Set Y-Limits for axis 3
l = size(torque2);
h.xlim([min(x12),max(x12)+50]);
% h.ylim(2,[0,100]); % Set Y-Limits for axis 4

h.gridon % Enable grid (use h.gridoff to remove)

% Modify the y-Axis Color
h.ycolor(1,'b'); % torque
h.ycolor(2,[0.4660 0.6740 0.1880]); % efficiency
h.ycolor(3,[0.3010 0.7450 0.9330]); % current
h.ycolor(4,'r'); % voltage
h.ycolor(5,'m'); % power in

% Add y-Labels
% h.ylabel(1,'Speed (RPM)');
h.ylabel(1, 'TL (Nm)');
h.ylabel(2,'Efficiency (%)');
h.ylabel(3,'Current (A)');
h.ylabel(4,'Voltage (volt)');
h.ylabel(5,'Pin (W)');

% Add x-Label
% h.xlabel('TL (Nm)');
h.xlabel('Speed (RPM)');

% Add title
title('TNcurve of Shunt Excited Motor');
set(gca,'FontWeight','bold','FontSize',14);

% Change Position of the whole myaxisc-Object
h.position([0.1,0.1,0.8,0.8],0.12); % Position-Vector and Spacing 0.12

% Change all font sizes
h.fontsize(10)

%% DataSaving
time = out.tout;
powerout2 = out.Pout2;
powerin2 = out.Pin2;
speed2 = out.omega2;
efficiency2 = out.Eff2;
voltage2 = out.Vs;
current2 = out.Ia2;
% 
% filename = 'Shunt_TNcurve_DataSave.csv';
% savedata = [time, powerin2, powerout2, speed2, efficiency2, voltage2, current2];
% writematrix(savedata, filename);
print('-dpng', '-r300', '../static/output_ShuntExcited.png');
close(fig);
