clc; clear;

% 設定參數（註解掉的部分）
% L = 0.013242
% R = 3.2645
% J = 0.01829
% B = 0.019
% Ke = 1.1895
% Kt = 1.1895
% simulation_time = 150



% 執行 Simulink 模型模擬
out = sim('SeriesExcited_model');


%% Data Loading

tl1 = out.Tl1;
f1 = size(tl1);

% clear datas 
torque1 = 0;
x11 = 0;
y11 = 0; y21 = 0; y31 = 0; y41 = 0; y51 = 0; y61 = 0;

switch LoadMode   % mode ( 1:ramp load , 2:stair load )

    case 1  

        i = 1;
        while 1
            if tl1(i) > 0.01
               s = i;
               break
            end
            i = i+1;
        end
        torque1 = out.Tl1(s:f1(1));
        x11 = out.omega1(s:f1(1));
        % y11 = out.omega1(s:f1(1));
        y21 = out.Eff1(s:f1(1));
        y31 = out.Pin1(s:f1(1));
        y41 = out.Pout1(s:f1(1));
        y51 = out.Vs(s:f1(1));
        y61 = out.Ia1(s:f1(1));
    case 2

        tl_pre1 = 0;
        j = 1;
        for i = 1:f1(1)           
            if tl1(i) > tl_pre1
                torque1(j,1) = tl1(i-1);
                x11(j,1) = out.omega1((i-1),1);
                % y11(j,1) = out.omega1((i-1),1);
                y21(j,1) = out.Eff1((i-1),1);
                y31(j,1) = out.Pin1((i-1),1);
                y41(j,1) = out.Pout1((i-1),1);
                y51(j,1) = out.Vs((i-1),1);
                y61(j,1) = out.Ia1((i-1),1);
                j = j+1;
            end
            tl_pre1 = tl1(i);
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
        p(1) = plot(h.p(1),x11,torque1,'b','LineWidth',1.2);
        p(2) = plot(h.p(2),x11,y21,'Color',[0.4660 0.6740 0.1880],'LineWidth',1.2);
        p(3) = plot(h.p(3),x11,y61,'Color',[0.3010 0.7450 0.9330],'LineWidth',1.2);
        p(4) = plot(h.p(4),x11,y51,'r','LineWidth',1.2);
        p(5) = plot(h.p(5),x11,y31,'m','LineWidth',1.2);
        print("case1");

    case 2
        p(1) = plot(h.p(1),x11,torque1,'b-*','LineWidth',1.1);
        p(2) = plot(h.p(2),x11,y21,'-*','Color',[0.4660 0.6740 0.1880],'LineWidth',1.1);
        p(3) = plot(h.p(3),x11,y61,'-*','Color',[0.3010 0.7450 0.9330],'LineWidth',1.1);
        p(4) = plot(h.p(4),x11,y51,'r-*','LineWidth',1.1);
        p(5) = plot(h.p(5),x11,y31,'m-*','LineWidth',1.1);
        print("case2");

end

h.autoscale % Automatically Scale Y Axis

% Automatically Scale Y Axis
for i = 1:5
    h.autoy(i);
end

h.xlim([min(x11),max(x11)+50]);
l = size(torque1);
h.xlim([min(x11),max(x11)+50]);

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
title('TNcurve of Series Excited Motor');
set(gca,'FontWeight','bold','FontSize',14);

% Change Position of the whole myaxisc-Object
h.position([0.1,0.1,0.8,0.8],0.12); % Position-Vector and Spacing 0.12

% Change all font sizes
h.fontsize(10)

%% DataSaving
time = out.tout;
powerin1 = out.Pin1;
powerout1 = out.Pout1;
speed1 = out.omega1;
efficiency1 = out.Eff1;
voltage1 = out.Vs;
current1 = out.Ia1;

% filename = 'Series_TNcurve_DataSave.csv';
% savedata = [time, powerin1, powerout1, speed1, efficiency1, voltage1, current1];
% writematrix(savedata, filename);

% 儲存圖形並關閉
print('-dpng', '-r300', '../static/output_SeriesExcited.png');
close(fig);