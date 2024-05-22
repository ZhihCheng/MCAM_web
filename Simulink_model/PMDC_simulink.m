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
out = sim("PMDC_model");

%% Data Loading

tl = out.Tl;
f = size(tl);

% clear datas 
torque = 0;
x1 = 0;
y1 = 0; y2 = 0; y3 = 0; y4 = 0; y5 = 0; y6 = 0;

switch LoadMode   % mode ( 1:ramp load , 2:stair load )

    case 1  

        i = 1;
        while 1
            if tl(i) > 0.01
               s = i;
               break
            end
            i = i+1;
        end
        torque = out.Tl(s:f(1));
        x1 = out.omega(s:f(1));
        % y1 = out.Tl(s:f(1));
        y2 = out.Eff(s:f(1));
        y3 = out.Pin(s:f(1));
        y4 = out.Pout(s:f(1));
        y5 = out.Vs(s:f(1));
        y6 = out.Ia(s:f(1));
        case 2

        tl_pre = 0;
        j = 1;
        for i = 1:f(1)           
            if tl(i) > tl_pre
                torque(j,1) = tl(i-1);
                x1(j,1) = out.omega((i-1),1);
                % y1(j,1) = out.tl((i-1),1);
                y2(j,1) = out.Eff((i-1),1);
                y3(j,1) = out.Pin((i-1),1);
                y4(j,1) = out.Pout((i-1),1);
                y5(j,1) = out.Vs((i-1),1);
                y6(j,1) = out.Ia((i-1),1);
                j = j+1;
            end
            tl_pre = tl(i);
        end
end

%% Plot
% plot TN curve

fig = figure('Visible', 'off');
set(gcf, 'Position', [200, 300, 1000, 500]); % [left, bottom, width, height]
% figure(2);
clf;

% Create empty axis system with 4 y axis by calling:
% handle = maxis(number of axis, y-spacing between outside lines)
h = myaxisc(5,0.10,[0.1,0.1,0.8,0.8]); % Specify position

% Call plot and specify y-axis number using method h.p(nr). For creating a
% legend later, we need to assign the handles returned by plot to p.
switch PlotMode

    case 1  
        p(1) = plot(h.p(1),x1,torque,'b','LineWidth',1.2);
        p(2) = plot(h.p(2),x1,y2,'Color',[0.4660 0.6740 0.1880],'LineWidth',1.2);
        p(3) = plot(h.p(3),x1,y6,'Color',[0.3010 0.7450 0.9330],'LineWidth',1.2);
        p(4) = plot(h.p(4),x1,y5,'r','LineWidth',1.2);
        p(5) = plot(h.p(5),x1,y3,'m','LineWidth',1.2);
        print("case1");

    case 2
        p(1) = plot(h.p(1),x1,torque,'b-*','LineWidth',1.1);
        p(2) = plot(h.p(2),x1,y2,'-*','Color',[0.4660 0.6740 0.1880],'LineWidth',1.1);
        p(3) = plot(h.p(3),x1,y6,'-*','Color',[0.3010 0.7450 0.9330],'LineWidth',1.1);
        p(4) = plot(h.p(4),x1,y5,'r-*','LineWidth',1.1);
        p(5) = plot(h.p(5),x1,y3,'m-*','LineWidth',1.1);
        print("case2");

end

% Automatically Scale Y Axis
for i = 1:5
    h.autoy(i);
end

l = size(torque);
h.xlim([min(x1),max(x1)+50]);

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
title('TNcurve of PMDC Motor');
set(gca,'FontWeight','bold','FontSize',14);

% Change Position of the whole myaxisc-Object
h.position([0.1,0.1,0.8,0.8],0.12); % Position-Vector and Spacing 0.12

% Change all font sizes
h.fontsize(10)

%% DataSaving
time = out.tout;
powerin = out.Pin;
powerout = out.Pout;
speed = out.omega;
efficiency = out.Eff;
voltage = out.Vs;
current = out.Ia;

% filename = 'PMDC_TNcurve_DataSave.csv';
% savedata = [time, powerin, powerout, speed, efficiency, voltage, current];
% writematrix(savedata, filename);

% 儲存圖形並關閉
print('-dpng', '-r300', '../static/output_PMDC.png');
close(fig);
