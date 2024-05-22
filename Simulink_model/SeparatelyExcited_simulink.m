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
out = sim("SeparatelyExcited_model");


%% Data Loading

tl3 = out.Tl3;
f3 = size(tl3);

% clear datas 
torque3 = 0;
x13 = 0;
y13 = 0; y23 = 0; y33 = 0; y43 = 0; y53 = 0; y63 = 0;

switch LoadMode   % mode ( 1:ramp load , 2:stair load )

    case 1  

        i = 1;
        while 1
            if tl3(i) > 0.01
               s = i;
               break
            end
            i = i+1;
        end
        torque3 = out.Tl3(s:f3(1));
        x13 = out.omega3(s:f3(1));
        % y13 = out.omega3(s:f3(1));
        y23 = out.Eff3(s:f3(1));
        y33 = out.Pin3(s:f3(1));
        y43 = out.Pout3(s:f3(1));
        y53 = out.Vs(s:f3(1));
        y63 = out.Ia3(s:f3(1));
        case 2

        tl_pre3 = 0;
        j = 1;
        for i = 1:f3(1)           
            if tl3(i) > tl_pre3
                torque3(j,1) = tl3(i-1);
                x13(j,1) = out.omega3((i-1),1);
                % y13(j,1) = out.omega3((i-1),1);
                y23(j,1) = out.Eff3((i-1),1);
                y33(j,1) = out.Pin3((i-1),1);
                y43(j,1) = out.Pout3((i-1),1);
                y53(j,1) = out.Vs((i-1),1);
                y63(j,1) = out.Ia3((i-1),1);
                j = j+1;
            end
            tl_pre3 = tl3(i);
        end
end

%% Plot
% plot TN curve

% figure(1);

fig = figure('Visible', 'off');
set(gcf, 'Position', [1050, 300, 1000, 500]); % [left, bottom, width, height]
clf;

% Create empty axis system with 4 y axis by calling:
% handle = maxis(number of axis, y-spacing between outside lines)
h = myaxisc(5,0.10,[0.1,0.1,0.8,0.8]); % Specify position

% Call plot and specify y-axis number using method h.p(nr). For creating a
% legend later, we need to assign the handles returned by plot to p.
switch PlotMode

    case 1  
        p(1) = plot(h.p(1),x13,torque3,'b','LineWidth',1.2);
        p(2) = plot(h.p(2),x13,y23,'Color',[0.4660 0.6740 0.1880],'LineWidth',1.2);
        p(3) = plot(h.p(3),x13,y63,'Color',[0.3010 0.7450 0.9330],'LineWidth',1.2);
        p(4) = plot(h.p(4),x13,y53,'r','LineWidth',1.2);
        p(5) = plot(h.p(5),x13,y33,'m','LineWidth',1.2);
        print("case1");

    case 2
        p(1) = plot(h.p(1),x13,torque3,'b-*','LineWidth',1.1);
        p(2) = plot(h.p(2),x13,y23,'-*','Color',[0.4660 0.6740 0.1880],'LineWidth',1.1);
        p(3) = plot(h.p(3),x13,y63,'-*','Color',[0.3010 0.7450 0.9330],'LineWidth',1.1);
        p(4) = plot(h.p(4),x13,y53,'r-*','LineWidth',1.1);
        p(5) = plot(h.p(5),x13,y33,'m-*','LineWidth',1.1);
        print("case2");

end

h.autoscale % Automatically Scale Y Axis

% Additional methods to modify appearance, scaling and so on:

% h.autoy(3) % Autoscale only specified y-axis
%h.ylim(3,[95,105]); % Set Y-Limits for axis 3
l3 = size(torque3);
h.xlim([min(x13),max(x13)]);
% h.ylim(2,[0,100]); % Set Y-Limits for axis 4
for i = 1:5
    h.autoy(i);
end

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
title('TNcurve of Separately Excited Motor');
set(gca,'FontWeight','bold','FontSize',14);

% Change Position of the whole myaxisc-Object
h.position([0.1,0.1,0.8,0.8],0.12); % Position-Vector and Spacing 0.12

% Change all font sizes
h.fontsize(10)

%% DataSaving
time = out.tout;
powerin3 = out.Pin3;
powerout3 = out.Pout3;
speed3 = out.omega3;
efficiency3 = out.Eff3;
voltage3 = out.Vs;
current3 = out.Ia3;

% filename = 'Seperately_TNcurve_DataSave.csv';
% savedata = [time, powerin3, powerout3, speed3, efficiency3, voltage3, current3];
% writematrix(savedata, filename);

% 儲存圖形並關閉
print('-dpng', '-r300', '../static/output_SeparatelyExcited.png');
close(fig);