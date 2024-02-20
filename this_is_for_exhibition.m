% clc;clear;

% L = 0.013242
% R = 3.2645
% J = 0.01829
% B = 0.019
% Ke = 1.1895
% Kt = 1.1895
% simulation_time =150


out = sim("./PMDC_exhibition.slx");

% Data Loading
tl = out.Tl;
f = size(tl);

% clear datas 
torque = 0;
y1 = 0; y2 = 0; y3 = 0; y4 = 0;

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
        y1 = out.omega(s:f(1));
        y2 = out.Eff(s:f(1));
        y3 = out.Pin(s:f(1));
        y4 = out.Pout(s:f(1));
        case 2

        tl_pre = 0;
        j = 1;
        for i = 1:f(1)           
            if tl(i) > tl_pre
                torque(j,1) = tl(i-1);
                y1(j,1) = out.omega((i-1),1);
                y2(j,1) = out.Eff((i-1),1);
                y3(j,1) = out.Pin((i-1),1);
                y4(j,1) = out.Pout((i-1),1);
                j = j+1;
            end
            tl_pre = tl(i);
        end
end

%% Plot
% plot TN curve

fig = figure('Visible', 'off');

% figure(2);
clf;

% Create empty axis system with 4 y axis by calling:
% handle = maxis(number of axis, y-spacing between outside lines)
h = myaxisc(4,0.10,[0.1,0.1,0.8,0.8]); % Specify position

% Call plot and specify y-axis number using method h.p(nr). For creating a
% legend later, we need to assign the handles returned by plot to p.
switch PlotMode

    case 1  
        p(1) = plot(h.p(1),torque,y1,'b','LineWidth',1.2);
        p(2) = plot(h.p(2),torque,y2,'Color',[0.4660 0.6740 0.1880],'LineWidth',1.2);
        p(3) = plot(h.p(3),torque,y3,'r','LineWidth',1.2);
        p(4) = plot(h.p(4),torque,y4,'Color',[0.9290 0.6940 0.1250],'LineWidth',1.2);
        print("case1");

    case 2
        p(1) = plot(h.p(1),torque,y1,'b-*','LineWidth',1.1);
        p(2) = plot(h.p(2),torque,y2,'-*','Color',[0.4660 0.6740 0.1880],'LineWidth',1.1);
        p(3) = plot(h.p(3),torque,y3,'r-*','LineWidth',1.1);
        p(4) = plot(h.p(4),torque,y4,'-*','Color',[0.9290 0.6940 0.1250],'LineWidth',1.1);
        print("case2");

end

h.autoscale % Automatically Scale Y Axis

% Additional methods to modify appearance, scaling and so on:

h.autoy(3) % Autoscale only specified y-axis
%h.ylim(3,[95,105]); % Set Y-Limits for axis 3
l = size(torque);
h.xlim([0,torque(l(1),1)+0.05]);
h.ylim(2,[0,100]); % Set Y-Limits for axis 4

h.gridon % Enable grid (use h.gridoff to remove)

% Modify the y-Axis Color
h.ycolor(1,'b');
h.ycolor(2,[0.4660 0.6740 0.1880]);
h.ycolor(3,'r');
h.ycolor(4,[0.9290 0.6940 0.1250]);

% Add y-Labels
h.ylabel(1,'Speed (RPM)');
h.ylabel(2,'Efficiency (%)');
h.ylabel(3,'Pin (W)');
h.ylabel(4,'Pout (W)');

% Add x-Label
h.xlabel('TL (Nm)');

% Change Position of the whole myaxisc-Object
h.position([0.1,0.1,0.8,0.8],0.12); % Position-Vector and Spacing 0.12

% Change all font sizes
h.fontsize(10)

print('-dpng', '-r300', './static/output_figure.png');
close(fig);